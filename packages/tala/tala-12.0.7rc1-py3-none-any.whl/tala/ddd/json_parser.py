import copy

from tala.model import move
from tala.model.plan_item import PlanItem, AssumePlanItem, AssumeIssuePlanItem, AssumeSharedPlanItem, \
    BindPlanItem, DoPlanItem, EmitIcmPlanItem, RespondPlanItem, ForgetPlanItem, ForgetAllPlanItem, \
    ForgetIssuePlanItem, IfThenElse, JumpToPlanItem, InvokeServiceQueryPlanItem, InvokeServiceActionPlanItem, \
    LogPlanItem, ForgetSharedPlanItem, GoalPerformedPlanItem, GoalAbortedPlanItem, ChangeDDDPlanItem
from tala.model.individual import No, Yes
from tala.model.question import Question, WhQuestion, YesNoQuestion, ConsequentQuestion, AltQuestion, \
    KnowledgePreconditionQuestion
from tala.model.lambda_abstraction import LambdaAbstractedProposition, \
    LambdaAbstractedImplicationPropositionForConsequent, LambdaAbstractedGoalProposition
from tala.model.question_raising_plan_item import FindoutPlanItem, RaisePlanItem
from tala.model.proposition import Proposition, GoalProposition, PropositionSet, \
    ResolvednessProposition, PrereportProposition, ImplicationProposition, UnderstandingProposition, \
    KnowledgePreconditionProposition, PreconfirmationProposition, RejectedPropositions, ServiceResultProposition, \
    ActionStatusProposition, ServiceActionStartedProposition, ServiceActionTerminatedProposition
from tala.model.polarity import Polarity
from tala.model.goal import Goal, PerformGoal, ResolveGoal
from tala.model.set import Set
from tala.model.date_time import DateTime
from tala.model.person_name import PersonName
from tala.model.service_action_outcome import SuccessfulServiceAction, FailedServiceAction
from tala.model.action_status import ActionStatus, Aborted, Done


class JSONParseFailure(Exception):
    pass


def preprocess_json_dict(json_dict_original):
    json_dict = copy.copy(json_dict_original)
    for float_key in ["perception_confidence", "understanding_confidence"]:
        if float_key in json_dict:
            try:
                json_dict[float_key] = float(json_dict[float_key])
            except TypeError:
                pass
    return json_dict


class JSONParser():
    def __init__(self, ddd_name, ontology, domain_name):
        self._ddd_name = ddd_name
        self.ontology = ontology
        self.ontology_name = ontology.get_name()
        self.domain_name = domain_name

    def parse(self, json_dict_unchecked):
        def is_plan_item():
            for item in PlanItem.ALL_PLAN_ITEM_TYPES:
                if item in json_dict:
                    return True
            return False

        def is_individual():
            return "value" in json_dict and "sort" in json_dict

        def is_yes_no():
            """ This is the template for extending the semantic object JSON
            with type information, which should be done for all semantic objects.
            """

            return json_dict.get("semantic_object_type") == "yes/no"

        def is_move():
            return "move_type" in json_dict

        def is_action():
            return "value" in json_dict

        def is_goal():
            return "_goal_type" in json_dict

        def is_question():
            question_type = json_dict.get("_type", None)
            return question_type in Question.TYPES

        def is_predicate():
            return "name" in json_dict and "sort" in json_dict

        def is_lambda_abstracted_proposition():
            return json_dict.get("semantic_object_type") == "LambdaAbstractedProposition"

        def is_set():
            return "set" in json_dict

        def is_service_action_outcome():
            return "service_action_outcome" in json_dict

        def is_proposition():
            prop_type = json_dict.get("_type", None)
            return prop_type in Proposition.TYPES

        def is_proposition_set():
            return "_propositions" in json_dict

        def is_action_status():
            return "action_status" in json_dict

        json_dict = preprocess_json_dict(json_dict_unchecked)
        if is_plan_item():
            return self.parse_plan_item(json_dict)
        if is_individual():
            return self.parse_individual(json_dict)
        if is_set():
            return self.parse_set(json_dict["set"])
        if is_move():
            return self.parse_move(json_dict)
        if is_action():
            return self.parse_action(json_dict)
        if is_goal():
            return self.parse_goal(json_dict)
        if is_question():
            return self.parse_question(json_dict)
        if is_predicate():
            return self.parse_predicate(json_dict)
        if is_proposition_set():
            return self.parse_proposition_set(json_dict)
        if is_proposition():
            return self.parse_proposition(json_dict)
        if is_lambda_abstracted_proposition():
            return self.parse_lambda_abstraction(json_dict)
        if is_service_action_outcome():
            return self.parse_service_action_outcome(json_dict)
        if is_yes_no():
            if json_dict["instance"] == No.NO:
                return No()
            if json_dict["instance"] == Yes.YES:
                return Yes()
        if is_action_status():
            return self.parse_action_status(json_dict)

        raise JSONParseFailure(f"JSONParser cannot parse: {json_dict}")

    def parse_plan_item(self, data):
        if PlanItem.TYPE_FINDOUT in data:
            return self.parse_findout_plan_item(data[PlanItem.TYPE_FINDOUT])
        if PlanItem.TYPE_RAISE in data:
            return self.parse_raise_plan_item(data[PlanItem.TYPE_RAISE])
        if PlanItem.TYPE_RESPOND in data:
            return self.parse_respond_plan_item(data[PlanItem.TYPE_RESPOND])
        if PlanItem.TYPE_ASSUME in data:
            return self.parse_assume_plan_item(data[PlanItem.TYPE_ASSUME])
        if PlanItem.TYPE_ASSUME_ISSUE in data:
            return self.parse_assume_issue_plan_item(data[PlanItem.TYPE_ASSUME_ISSUE])
        if PlanItem.TYPE_ASSUME_SHARED in data:
            return self.parse_assume_shared_plan_item(data[PlanItem.TYPE_ASSUME_SHARED])
        if PlanItem.TYPE_BIND in data:
            return self.parse_bind_plan_item(data[PlanItem.TYPE_BIND])
        if PlanItem.TYPE_DO in data:
            return self.parse_do_plan_item(data[PlanItem.TYPE_DO])
        if PlanItem.TYPE_EMIT_ICM in data:
            return self.parse_emit_icm_plan_item(data[PlanItem.TYPE_EMIT_ICM])
        if PlanItem.TYPE_FORGET in data:
            return self.parse_forget_plan_item(data[PlanItem.TYPE_FORGET])
        if PlanItem.TYPE_FORGET_SHARED in data:
            return self.parse_forget_shared_plan_item(data[PlanItem.TYPE_FORGET_SHARED])
        if PlanItem.TYPE_FORGET_ALL in data:
            return self.parse_forget_all_plan_item(data[PlanItem.TYPE_FORGET_ALL])
        if PlanItem.TYPE_FORGET_ISSUE in data:
            return self.parse_forget_issue_plan_item(data[PlanItem.TYPE_FORGET_ISSUE])
        if PlanItem.TYPE_IF_THEN_ELSE in data:
            return self.parse_if_then_else_plan_item(data[PlanItem.TYPE_IF_THEN_ELSE])
        if PlanItem.TYPE_JUMPTO in data:
            return self.parse_jumpto_plan_item(data[PlanItem.TYPE_JUMPTO])
        if PlanItem.TYPE_INVOKE_SERVICE_QUERY in data:
            return self.parse_invoke_service_query_plan_item(data[PlanItem.TYPE_INVOKE_SERVICE_QUERY])
        if PlanItem.TYPE_INVOKE_SERVICE_ACTION in data:
            return self.parse_invoke_service_action_plan_item(data[PlanItem.TYPE_INVOKE_SERVICE_ACTION])
        if PlanItem.TYPE_LOG in data:
            return self.parse_log_plan_item(data[PlanItem.TYPE_LOG])
        if PlanItem.TYPE_ACTION_PERFORMED in data:
            return self.parse_action_performed_plan_item(data[PlanItem.TYPE_ACTION_PERFORMED])
        if PlanItem.TYPE_ACTION_ABORTED in data:
            return self.parse_action_aborted_plan_item(data[PlanItem.TYPE_ACTION_ABORTED])
        if PlanItem.TYPE_CHANGE_DDD in data:
            return self.parse_change_ddd_plan_item(data[PlanItem.TYPE_CHANGE_DDD])
        raise JSONParseFailure(f"PlanItem {data} not supported by json parser")

    def parse_findout_plan_item(self, data):
        question = self.parse_question(data)
        return FindoutPlanItem(self.domain_name, question)

    def parse_raise_plan_item(self, data):
        question = self.parse_question(data)
        return RaisePlanItem(self.domain_name, question)

    def parse_respond_plan_item(self, data):
        question = self.parse_question(data)
        return RespondPlanItem(question)

    def parse_bind_plan_item(self, data):
        question = self.parse_question(data)
        return BindPlanItem(question)

    def parse_do_plan_item(self, data):
        action = self.parse_action(data)
        return DoPlanItem(action)

    def parse_log_plan_item(self, data):
        message = data
        return LogPlanItem(message)

    def parse_action_performed_plan_item(self, data):
        return GoalPerformedPlanItem(data)

    def parse_action_aborted_plan_item(self, data):
        return GoalAbortedPlanItem(data)

    def parse_change_ddd_plan_item(self, data):
        return ChangeDDDPlanItem(data)

    def parse_forget_plan_item(self, data):
        if "_type" in data.keys():
            proposition = self.parse_proposition(data)
            return ForgetPlanItem(proposition)
        else:
            predicate = self.parse_predicate(data)
            return ForgetPlanItem(predicate)

    def parse_forget_shared_plan_item(self, data):
        if "_type" in data.keys():
            proposition = self.parse_proposition(data)
            return ForgetSharedPlanItem(proposition)
        else:
            predicate = self.parse_predicate(data)
            return ForgetSharedPlanItem(predicate)

    def parse_forget_all_plan_item(self, _data):
        return ForgetAllPlanItem()

    def parse_forget_issue_plan_item(self, data):
        question = self.parse_question(data)
        return ForgetIssuePlanItem(question)

    def parse_assume_plan_item(self, data):
        proposition = self.parse_proposition(data)
        return AssumePlanItem(proposition)

    def parse_assume_issue_plan_item(self, data):
        question = self.parse_question(data)
        return AssumeIssuePlanItem(question)

    def parse_assume_shared_plan_item(self, data):
        proposition = self.parse_proposition(data)
        return AssumeSharedPlanItem(proposition)

    def parse_emit_icm_plan_item(self, data):
        icm = self.parse_move(data)
        return EmitIcmPlanItem(icm)

    def parse_jumpto_plan_item(self, data):
        goal = self.parse_goal(data)
        return JumpToPlanItem(goal)

    def parse_if_then_else_plan_item(self, data):
        condition = self.parse(data["condition"])
        consequent = [self.parse(element) for element in data["consequent"]]
        alternative = [self.parse(element) for element in data["alternative"]]
        return IfThenElse(condition, consequent, alternative)

    def parse_invoke_service_query_plan_item(self, data):
        issue = self.parse_question(data["issue"])
        min_results = int(data["min_results"])
        max_results = int(data["max_results"])
        return InvokeServiceQueryPlanItem(issue, min_results=min_results, max_results=max_results)

    def parse_invoke_service_action_plan_item(self, data):
        service_action = data["service_action"]
        preconfirm = data["preconfirm"]
        postconfirm = data["postconfirm"]
        downdate_plan = data["downdate_plan"]
        return InvokeServiceActionPlanItem(self.ontology_name, service_action, preconfirm, postconfirm, downdate_plan)

    def parse_lambda_abstraction(self, content):
        if content["type_"] == LambdaAbstractedProposition.LAMBDA_ABSTRACTED_PREDICATE_PROPOSITION:
            predicate = self.parse_predicate(content["predicate"])
            return self.ontology.create_lambda_abstracted_predicate_proposition(predicate)

        if content["type_"] == LambdaAbstractedProposition.LAMBDA_ABSTRACTED_GOAL_PROPOSITION:
            return LambdaAbstractedGoalProposition()

        if content["type_"] == LambdaAbstractedProposition.LAMBDA_ABSTRACTED_IMPLICATION_PROPOSITION_FOR_CONSEQUENT:
            antecedent = self.parse_proposition(content["_antecedent"])
            predicate = self.parse_predicate(content["_consequent_predicate"])
            return LambdaAbstractedImplicationPropositionForConsequent(antecedent, predicate, self.ontology_name)

    def parse_question(self, data):
        if data["_type"] == Question.TYPE_WH:
            lambda_abstraction = self.parse_lambda_abstraction(data["_content"])
            return WhQuestion(lambda_abstraction)
        if data["_type"] == Question.TYPE_KPQ:
            embedded_question = self.parse_question(data["_content"])
            return KnowledgePreconditionQuestion(embedded_question)
        if data["_type"] == Question.TYPE_YESNO:
            proposition = self.parse(data["_content"])
            return YesNoQuestion(proposition)
        if data["_type"] == Question.TYPE_ALT:
            p_set = self.parse_proposition_set(data["_content"])
            return AltQuestion(p_set)
        if data["_type"] == Question.TYPE_CONSEQUENT:
            lambda_abstraction = self.parse_lambda_abstraction(data["_content"])
            return ConsequentQuestion(lambda_abstraction)

    def parse_proposition_set(self, data):
        proposition_list = data["_propositions"]
        propositions = [self.parse_proposition(proposition) for proposition in proposition_list]
        polarity = data["_polarity"]
        return PropositionSet(propositions, polarity)

    def parse_set(self, data):
        result_set = Set([self.parse(element) for element in data])
        return result_set

    def parse_predicate(self, data):
        predicate_name = data["name"]
        return self.ontology.get_predicate(predicate_name)

    def parse_individual(self, data):
        def extract(string, prefix, suffix):
            if value.startswith(prefix) and value.endswith(suffix):
                return value[len(prefix):len(value) - len(suffix)]

        def extract_datetime_value():
            return extract(value, "datetime(", ")")

        def extract_person_name_value():
            return extract(value, "person_name(", ")")

        sort = self.ontology.get_sort(data["sort"]["_name"])
        value = data["value"]
        polarity = data["polarity"]
        if sort.is_datetime_sort():
            value = DateTime(extract_datetime_value())
        if sort.is_real_sort():
            value = float(value)
        if sort.is_person_name_sort():
            value = PersonName(extract_person_name_value())
        if sort.is_integer_sort():
            value = int(value)
        if polarity == Polarity.POS:
            return self.ontology.create_individual(value, sort)
        return self.ontology.create_negative_individual(value)

    def parse_move(self, data):
        if data["move_type"] == move.Move.ANSWER:
            return self.parse_answer_move(data)
        if data["move_type"] == move.Move.REQUEST:
            return self.parse_request_move(data)
        if data["move_type"] == move.Move.ASK:
            return self.parse_ask_move(data)
        if data["move_type"] == move.ICMMove.ACC:
            return self.parse_acc_icm(data)
        if data["move_type"] == move.ICMMove.ACCOMMODATE:
            return self.parse_accommodate_icm(data)
        if data["move_type"] == move.ICMMove.RESUME:
            return self.parse_resume_icm(data)
        if data["move_type"] == move.ICMMove.RERAISE:
            return self.parse_reraise_icm(data)
        if data["move_type"] == move.ICMMove.PER:
            return self.parse_per_icm(data)
        if data["move_type"] == move.ICMMove.UND:
            return self.parse_und_icm(data)
        if data["move_type"] == move.ICMMove.SEM:
            return self.parse_sem_icm(data)
        if data["move_type"] == move.ICMMove.LOADPLAN:
            return self.parse_loadplan_icm(data)
        if data["move_type"] == move.Move.GREET:
            return self.parse_greet_move(data)
        if data["move_type"] == move.Move.INSULT:
            return self.parse_insult_move(data)
        if data["move_type"] == move.Move.INSULT_RESPONSE:
            return self.parse_insult_response_move(data)
        if data["move_type"] == move.Move.MUTE:
            return self.parse_mute_move(data)
        if data["move_type"] == move.Move.UNMUTE:
            return self.parse_unmute_move(data)
        if data["move_type"] == move.Move.PREREPORT:
            return self.parse_prereport_move(data)
        if data["move_type"] == move.Move.REPORT:
            return self.parse_report_move(data)
        if data["move_type"] == move.Move.QUIT:
            return self.parse_quit_move(data)
        if data["move_type"] == move.Move.THANK_YOU:
            return self.parse_thank_you_move(data)
        if data["move_type"] == move.Move.THANK_YOU_RESPONSE:
            return self.parse_thank_you_response_move(data)

    def parse_answer_move(self, data):
        content = self.parse(data["content"])
        return move.AnswerMove(
            content,
            speaker=data["speaker"],
            understanding_confidence=data["understanding_confidence"],
            modality=data["modality"],
            ddd_name=data["ddd"],
            utterance=data["utterance"],
            perception_confidence=data["perception_confidence"]
        )

    def parse_request_move(self, data):
        action = self.parse_action(data["content"])
        return move.RequestMove(
            action,
            speaker=data["speaker"],
            understanding_confidence=data["understanding_confidence"],
            modality=data["modality"],
            ddd_name=data["ddd"],
            utterance=data["utterance"],
            perception_confidence=data["perception_confidence"]
        )

    def parse_proposition(self, data):
        if data["_type"] == Proposition.PREDICATE:
            if data["predicate"]["sort"]["_name"] == "boolean":
                individual = None
            else:
                individual = self.parse_individual(data["individual"])
            predicate = self.parse_predicate(data["predicate"])
            polarity = data.get("_polarity")
            return self.ontology.create_predicate_proposition(predicate, individual, polarity)
        if data["_type"] == Proposition.GOAL:
            goal = self.parse_goal(data["_content"])
            polarity = data.get("_polarity")
            return GoalProposition(goal, polarity)
        if data["_type"] == Proposition.PRECONFIRMATION:
            service_action = data.get("service_action")
            polarity = data.get("_polarity")
            arguments = [self.parse_proposition(proposition) for proposition in data.get("_arguments")]
            return PreconfirmationProposition(self.ontology_name, service_action, arguments, polarity)
        if data["_type"] == Proposition.SERVICE_RESULT:
            service_action = data.get("service_action")
            action_outcome = self.parse(data.get("result"))
            arguments = [self.parse_proposition(proposition) for proposition in data.get("arguments")]
            return ServiceResultProposition(self.ontology_name, service_action, arguments, action_outcome)
        if data["_type"] == Proposition.UNDERSTANDING:
            content = self.parse(data["_content"])
            polarity = data.get("_polarity")
            speaker = data.get("_speaker")
            return UnderstandingProposition(speaker, content, polarity)
        if data["_type"] == Proposition.RESOLVEDNESS:
            issue = self.parse_question(data["issue"])
            return ResolvednessProposition(issue)
        if data["_type"] == Proposition.KNOWLEDGE_PRECONDITION:
            question = self.parse_question(data["_content"])
            polarity = data.get("_polarity")
            return KnowledgePreconditionProposition(question, polarity)
        if data["_type"] == Proposition.ACTION_STATUS:
            status = self.parse_action_status(data["_status"])
            action = self.parse_action(data["_content"])
            return ActionStatusProposition(action, status)
        if data["_type"] == Proposition.SERVICE_ACTION_STARTED:
            service_action = data["service_action"]
            parameters = [self.parse_proposition(proposition) for proposition in data.get("parameters")]
            return ServiceActionStartedProposition(self.ontology_name, service_action, parameters)
        if data["_type"] == Proposition.SERVICE_ACTION_TERMINATED:
            service_action = data["service_action"]
            polarity = data.get("_polarity")
            return ServiceActionTerminatedProposition(self.ontology_name, service_action, polarity)
        if data["_type"] == Proposition.PREREPORT:
            service_action = data["service_action"]
            argument_list = [self.parse_proposition(proposition) for proposition in data["argument_set"]]
            return PrereportProposition(self.ontology_name, service_action, argument_list)
        if data["_type"] == Proposition.REJECTED:
            polarity = data.get("_polarity")
            reason_for_rejection = data.get("reason_for_rejection")
            combination = self.parse(data["rejected_combination"])
            return RejectedPropositions(combination, polarity, reason_for_rejection)
        if data["_type"] == Proposition.IMPLICATION:
            antecedent = self.parse_proposition(data["_antecedent"])
            consequent = self.parse_proposition(data["_consequent"])
            return ImplicationProposition(antecedent, consequent)

    def parse_goal(self, data):
        if data.get("_goal_type") == Goal.PERFORM_GOAL:
            target = data.get("_target")
            action = self.parse_action(data["_content"])
            return PerformGoal(action, target=target)
        if data.get("_goal_type") == Goal.RESOLVE_GOAL:
            target = data.get("_target")
            question = self.parse_question(data["_content"])
            return ResolveGoal(question, target=target)

    def parse_acc_icm(self, data):
        if data.get("content"):
            content = self.parse(data["content"])
            return move.ICMMoveWithContent(
                move.ICMMove.ACC,
                content,
                understanding_confidence=data["understanding_confidence"],
                speaker=data["speaker"],
                polarity=data["polarity"],
                ddd_name=data["ddd"],
                perception_confidence=data["perception_confidence"]
            )
        return move.ICMMove(
            move.ICMMove.ACC,
            understanding_confidence=data["understanding_confidence"],
            speaker=data["speaker"],
            polarity=data["polarity"],
            ddd_name=data["ddd"],
            perception_confidence=data["perception_confidence"]
        )

    def parse_accommodate_icm(self, data):
        if data.get("content"):
            content = self.parse(data["content"])
            return move.ICMMoveWithContent(
                move.ICMMove.ACCOMMODATE,
                content,
                understanding_confidence=data["understanding_confidence"],
                speaker=data["speaker"],
                polarity=data["polarity"],
                ddd_name=data["ddd"],
                perception_confidence=data["perception_confidence"]
            )
        else:
            return move.ICMMove(
                move.ICMMove.ACCOMMODATE,
                understanding_confidence=data["understanding_confidence"],
                speaker=data["speaker"],
                polarity=data["polarity"],
                ddd_name=data["ddd"],
                perception_confidence=data["perception_confidence"]
            )

    def parse_resume_icm(self, data):
        goal = self.parse_goal(data["content"])
        return move.ICMMoveWithContent(
            move.ICMMove.RESUME,
            goal,
            understanding_confidence=data["understanding_confidence"],
            speaker=data["speaker"],
            polarity=data["polarity"],
            ddd_name=data["ddd"],
            perception_confidence=data["perception_confidence"]
        )

    def parse_reraise_icm(self, data):
        if data.get("content"):
            action = self.parse(data["content"])
            return move.ICMMoveWithContent(
                move.ICMMove.RERAISE,
                action,
                understanding_confidence=data["understanding_confidence"],
                speaker=data["speaker"],
                polarity=data["polarity"],
                ddd_name=data["ddd"],
                perception_confidence=data["perception_confidence"]
            )
        else:
            return move.ICMMove(
                move.ICMMove.RERAISE,
                understanding_confidence=data["understanding_confidence"],
                speaker=data["speaker"],
                polarity=data["polarity"],
                ddd_name=data["ddd"],
                perception_confidence=data["perception_confidence"]
            )

    def parse_per_icm(self, data):
        string = data.get("content", None)
        if string:
            return move.ICMMoveWithContent(
                move.ICMMove.PER,
                string,
                understanding_confidence=data["understanding_confidence"],
                speaker=data["speaker"],
                polarity=data["polarity"],
                ddd_name=data["ddd"],
                perception_confidence=data["perception_confidence"]
            )
        return move.ICMMove(
            move.ICMMove.PER,
            understanding_confidence=data["understanding_confidence"],
            speaker=data["speaker"],
            polarity=data["polarity"],
            ddd_name=data["ddd"],
            perception_confidence=data["perception_confidence"]
        )

    def parse_und_icm(self, data):
        content_data = data["content"]
        if content_data:
            content = self.parse(content_data)
        else:
            content = None
        return move.ICMMoveWithSemanticContent(
            move.ICMMove.UND,
            content,
            content_speaker=data["content_speaker"],
            understanding_confidence=data["understanding_confidence"],
            speaker=data["speaker"],
            polarity=data["polarity"],
            ddd_name=data["ddd"],
            perception_confidence=data["perception_confidence"]
        )

    def parse_sem_icm(self, data):
        content_data = data["content"]
        if content_data:
            content = self.parse_proposition(content_data)
        else:
            content = None
        return move.ICMMoveWithSemanticContent(
            move.ICMMove.SEM,
            content,
            content_speaker=data["content_speaker"],
            understanding_confidence=data["understanding_confidence"],
            speaker=data["speaker"],
            polarity=data["polarity"],
            ddd_name=data["ddd"],
            perception_confidence=data["perception_confidence"]
        )

    def parse_loadplan_icm(self, data):
        return move.ICMMove(
            move.ICMMove.LOADPLAN,
            understanding_confidence=data["understanding_confidence"],
            speaker=data["speaker"],
            polarity=data["polarity"],
            ddd_name=data["ddd"],
            perception_confidence=data["perception_confidence"]
        )

    def parse_greet_move(self, data):
        return move.GreetMove(
            understanding_confidence=data["understanding_confidence"],
            speaker=data["speaker"],
            ddd_name=data["ddd"],
            perception_confidence=data["perception_confidence"]
        )

    def parse_insult_move(self, data):
        return move.InsultMove(
            understanding_confidence=data["understanding_confidence"],
            speaker=data["speaker"],
            ddd_name=data["ddd"],
            perception_confidence=data["perception_confidence"]
        )

    def parse_insult_response_move(self, data):
        return move.InsultResponseMove(
            understanding_confidence=data["understanding_confidence"],
            speaker=data["speaker"],
            ddd_name=data["ddd"],
            perception_confidence=data["perception_confidence"]
        )

    def parse_mute_move(self, data):
        return move.MuteMove(
            understanding_confidence=data["understanding_confidence"],
            speaker=data["speaker"],
            ddd_name=data["ddd"],
            perception_confidence=data["perception_confidence"]
        )

    def parse_unmute_move(self, data):
        return move.UnmuteMove(
            understanding_confidence=data["understanding_confidence"],
            speaker=data["speaker"],
            ddd_name=data["ddd"],
            perception_confidence=data["perception_confidence"]
        )

    def parse_quit_move(self, data):
        return move.QuitMove(
            understanding_confidence=data["understanding_confidence"],
            speaker=data["speaker"],
            ddd_name=data["ddd"],
            perception_confidence=data["perception_confidence"]
        )

    def parse_thank_you_move(self, data):
        return move.ThankYouMove(
            understanding_confidence=data["understanding_confidence"],
            speaker=data["speaker"],
            ddd_name=data["ddd"],
            perception_confidence=data["perception_confidence"]
        )

    def parse_thank_you_response_move(self, data):
        return move.ThankYouResponseMove(
            understanding_confidence=data["understanding_confidence"],
            speaker=data["speaker"],
            ddd_name=data["ddd"],
            perception_confidence=data["perception_confidence"]
        )

    def parse_prereport_move(self, data):
        service_action = data["service_action"]
        arguments = data["arguments"]
        argument_list = [self.parse_proposition(argument) for argument in arguments]
        return move.PrereportMove(self.ontology_name, service_action, argument_list)

    def parse_report_move(self, data):
        content = self.parse(data["content"])
        return move.ReportMove(content)

    def parse_action(self, data):
        action_name = data["value"]
        return self.ontology.create_action(action_name)

    def parse_ask_move(self, data):
        question = self.parse_question(data["content"])
        return move.AskMove(question, speaker=data["speaker"], modality=data["modality"], ddd_name=data["ddd"])

    def parse_service_action_outcome(self, json):
        if json["service_action_outcome"]:
            return SuccessfulServiceAction()
        return FailedServiceAction(json["failure_reason"])

    def parse_action_status(self, json):
        if json["action_status"] == ActionStatus.DONE:
            return Done()
        if json["action_status"] == ActionStatus.ABORTED:
            return Aborted(json["reason"])
