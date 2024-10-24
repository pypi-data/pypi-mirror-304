import React from "react";

import { i18next } from "@translations/oarepo_requests_ui/i18next";
import { List } from "semantic-ui-react";

/** 
 * @typedef {import("../types").Request} Request
 * @typedef {import("../types").RequestType} RequestType
 */

/** @param {{ request: Request, isSidebar: boolean }} props */
export const ModalContentSideInfo = ({ request, isSidebar = false }) => {
  return (
    <List divided={isSidebar} relaxed={isSidebar}>
      <List.Item>
        <List.Content>
          <List.Header>{i18next.t("Creator")}</List.Header>
          {request.created_by?.link && <a href={request.created_by.link}>{request.created_by.label}</a> || request.created_by?.label}
        </List.Content>
      </List.Item>
      <List.Item>
        <List.Content>
          <List.Header>{i18next.t("Receiver")}</List.Header>
          {request.receiver?.link && <a href={request.receiver?.link}>{request.receiver?.label}</a> || request.receiver?.label}
        </List.Content>
      </List.Item>
      <List.Item>
        <List.Content>
          <List.Header>{i18next.t("Request type")}</List.Header>
          {request.type}
        </List.Content>
      </List.Item>
      <List.Item>
        <List.Content>
          <List.Header>{i18next.t("Created")}</List.Header>
          {request?.created}
        </List.Content>
      </List.Item>
    </List>
  )
};
