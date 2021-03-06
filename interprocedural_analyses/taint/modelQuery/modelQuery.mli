(* Copyright (c) 2018-present, Facebook, Inc.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree. *)

val apply_query_rule
  :  resolution:Analysis.GlobalResolution.t ->
  rule:Taint.Model.ModelQuery.rule ->
  callable:Interprocedural.Callable.real_target ->
  (Taint.Model.annotation_kind * Taint.Model.taint_annotation) list

val apply_all_rules
  :  resolution:Analysis.Resolution.t ->
  scheduler:Scheduler.t ->
  configuration:Taint.TaintConfiguration.t ->
  rule_filter:int list option ->
  rules:Taint.Model.ModelQuery.rule list ->
  callables:Interprocedural.Callable.real_target list ->
  models:Taint.Result.call_model Interprocedural.Callable.Map.t ->
  skip_overrides:Ast.Reference.Set.t ->
  Taint.Result.call_model Interprocedural.Callable.Map.t * Ast.Reference.Set.t
