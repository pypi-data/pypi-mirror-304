// This file is part of Invenio-RDM-Records
// Copyright (C) 2020-2023 CERN.
// Copyright (C) 2020-2022 Northwestern University.
//
// Invenio-RDM-Records is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

import React from "react";
import ReactDOM from "react-dom";

import { Form, Formik } from "formik";

import { ResourceTypeField } from "./ResourceTypeField";

it("renders without crashing", () => {
  const div = document.createElement("div");
  const options = [
    {
      icon: "",
      id: "resource-type-id-A",
      type_name: "Type A",
      subtype_name: "Subtype A",
    },
    {
      icon: "frown outline",
      id: "resource-type-id-B",
      type_name: "Type B",
      subtype_name: "Subtype B",
    },
  ];

  ReactDOM.render(
    <Formik>
      {() => (
        <Form>
          <ResourceTypeField fieldPath="fieldPath" options={options} />
        </Form>
      )}
    </Formik>,
    div
  );
});
