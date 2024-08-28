"use client";
import React from "react";
import { Toaster } from "react-hot-toast";

function ToastProvider() {
  return (
    <div>
      <Toaster position="top-right" />
    </div>
  );
}

export default ToastProvider;
