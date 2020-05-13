/*!
 * Copyright (c) 2020 by Contributors
 * \file logging.cc
 * \author Hyunsu Cho
 * \brief logging facility for Treelite
 */

#include <dmlc/logging.h>
#include <treelite/logging.h>

// Override logging mechanism
void dmlc::CustomLogMessage::Log(const std::string& msg) {
  const treelite::LogCallbackRegistry* registry
    = treelite::LogCallbackRegistryStore::Get();
  auto callback = registry->Get();
  callback(msg.c_str());
}
