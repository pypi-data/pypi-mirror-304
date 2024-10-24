import React, { useState, useCallback } from "react";

import _isEmpty from "lodash/isEmpty";
import axios from "axios";

import { i18next } from "@translations/oarepo_requests_ui/i18next";
import { Button } from "semantic-ui-react";
import { useFormikContext } from "formik";

import { isDeepEmpty } from "../utils";
import { useConfirmModalContext } from "../contexts";
import { REQUEST_TYPE } from "./objects";

/** 
 * @typedef {import("semantic-ui-react").ConfirmProps} ConfirmProps
 */

export const useConfirmDialog = (isEventModal = false) => {
  const { setSubmitting } = useFormikContext();

  /** @type {[ConfirmProps, (props: ConfirmProps) => void]} */
  const [confirmDialogProps, setConfirmDialogProps] = useState({
    open: false,
    content: i18next.t("Are you sure?"),
    cancelButton: i18next.t("Close"),
    confirmButton: i18next.t("OK"),
    onCancel: () => setConfirmDialogProps(props => ({ ...props, open: false })),
    onConfirm: () => setConfirmDialogProps(props => ({ ...props, open: false }))
  });

  const confirmAction = useCallback((onConfirm, requestType, createAndSubmit = false) => {
    /** @type {ConfirmProps} */
    let newConfirmDialogProps = {
      open: true,
      onConfirm: () => {
        setConfirmDialogProps(props => ({ ...props, open: false }));
        onConfirm();
      },
      onCancel: () => {
        setConfirmDialogProps(props => ({ ...props, open: false }));
        setSubmitting(false);
      }
    };

    switch (requestType) {
      case REQUEST_TYPE.CREATE:
        newConfirmDialogProps.header = isEventModal ? i18next.t("Submit event") : i18next.t("Create request");
        break;
      case REQUEST_TYPE.SUBMIT:
        newConfirmDialogProps.header = i18next.t("Submit request");
        newConfirmDialogProps.confirmButton = i18next.t("OK");
        break;
      case REQUEST_TYPE.CANCEL:
        newConfirmDialogProps.header = i18next.t("Cancel request");
        newConfirmDialogProps.confirmButton = <Button negative>{i18next.t("Cancel request")}</Button>;
        break;
      case REQUEST_TYPE.ACCEPT:
        newConfirmDialogProps.header = i18next.t("Accept request");
        newConfirmDialogProps.confirmButton = <Button positive>{i18next.t("Accept")}</Button>;
        break;
      case REQUEST_TYPE.DECLINE:
        newConfirmDialogProps.header = i18next.t("Decline request");
        newConfirmDialogProps.confirmButton = <Button negative>{i18next.t("Decline")}</Button>;
        break;
      default:
        break;
    }

    if (createAndSubmit) {
      newConfirmDialogProps = {
        ...newConfirmDialogProps,
        header: i18next.t("Create and submit request"),
        confirmButton: <Button positive>{i18next.t("Create and submit")}</Button>,
        onConfirm: () => {
          setConfirmDialogProps(props => ({ ...props, open: false }));
          onConfirm();
        }
      }
    }

    setConfirmDialogProps(props => ({ ...props, ...newConfirmDialogProps }));
  }, [setSubmitting, isEventModal]);

  return { confirmDialogProps, confirmAction };
}

export const useRequestsApi = (request, onSubmit) => {
  const {
    values: formValues,
    resetForm,
    setSubmitting,
    setErrors,
  } = useFormikContext();
  const { confirmAction } = useConfirmModalContext();

  const setError = error => { setErrors({ api: error }); };

  const callApi = async (url, method, data = formValues, doNotHandleResolve = false) => {
    const promise = axios({
      method: method,
      url: url,
      data: data,
      headers: { 'Content-Type': 'application/json' }
    });

    if (doNotHandleResolve) {
      return promise;
    }

    return promise
      .then(() => {
        resetForm();
      })
      .catch(error => {
        setError(error);
        throw error;
      });
  };

  const createAndSubmitRequest = () => onSubmit(async () => {
      const createdRequest = await callApi(request.links?.actions?.create, 'post', formValues, true);
      await callApi(createdRequest.data?.links?.actions?.submit, 'post', {}, true);
      resetForm();
    }, (error) => {
      setError(error);
    });

  const doCreateAndSubmitAction = (waitForConfirmation = false) => {
    setSubmitting(true);
    setErrors({});
    if (waitForConfirmation) {
      confirmAction(createAndSubmitRequest, REQUEST_TYPE.SUBMIT, true);
    } else {
      createAndSubmitRequest();
    }
  };

  const sendRequest = async (actionUrl, requestType) => {
    actionUrl = request.links?.actions[requestType];
    if (requestType === REQUEST_TYPE.SAVE) {
      return callApi(actionUrl, 'put');
    } else if (requestType === REQUEST_TYPE.ACCEPT) { // Reload page after succesful "Accept" operation
      await callApi(actionUrl, 'post');
      window.location.reload();
      return;
    }
    const mappedData = !isDeepEmpty(formValues) ? {} : formValues;
    return callApi(actionUrl, 'post', mappedData);
  };

  const doAction = async (requestType, waitForConfirmation = false) => {
    const actionUrl = request.links.actions[requestType];
    if (waitForConfirmation) {
      confirmAction(() => onSubmit(() => sendRequest(actionUrl, requestType)), requestType);
    } else {
      onSubmit(() => sendRequest(actionUrl, requestType));
    }
  };

  return { doAction, doCreateAndSubmitAction };
}