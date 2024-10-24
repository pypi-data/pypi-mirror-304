import React from "react";

import { i18next } from "@translations/oarepo_requests_ui/i18next";
import { Segment, Header, Placeholder, Message } from "semantic-ui-react";
import _isEmpty from "lodash/isEmpty";

import { RequestList } from ".";
import { useRequestContext } from "../contexts";

/**
 * @typedef {import("../types").Request} Request
 * @typedef {import("../types").RequestType} RequestType
 */
/**
 * @param {{ requestTypes: RequestType[], isLoading: boolean, loadingError: Error }} props
 */
export const RequestListContainer = ({ requestsLoading, requestsLoadingError }) => {
  const { requests } = useRequestContext();
  let openRequests = requests.filter(request => request.is_open || request?.status_code.toLowerCase() === "created");

  return (
    (requestsLoading || requestsLoadingError || !_isEmpty(openRequests)) &&
    <Segment className="requests-my-requests borderless">
      <Header size="tiny" className="detail-sidebar-header">{i18next.t("Pending")}</Header>
      {requestsLoading ?
        <Placeholder fluid>
          {Array.from({ length: 2 }).map((_, index) => (
            <Placeholder.Paragraph key={index}>
              <Placeholder.Line length="full" />
              <Placeholder.Line length="medium" />
            </Placeholder.Paragraph>
          ))} 
        </Placeholder> :
        requestsLoadingError ?
          <Message negative>
            <Message.Header>{i18next.t("Error loading requests")}</Message.Header>
            <p>{requestsLoadingError?.message}</p>
          </Message> :
          <RequestList requests={openRequests} />
      }
    </Segment>
  );
};
