####################
# Scores Tests
####################

# Test Suite Control Scores
SUITE_NAME = "Scores"
SUITE_TEST_ID = global_catalog_entity
SUITE_TEST_NAME = SUITE_TEST_ID.replace("_", " ").capitalize()
SUITE_TEST_CLASS = client.scores
SUITE_CREATE_OBJECT = ScoreCreateRequest(
    identifier=SUITE_TEST_ID, name=SUITE_TEST_NAME, kind="component"
)

LIST_KWARGS = {"kind": SUITE_CREATE_OBJECT.kind}
GET_KWARGS = {"kind": SUITE_CREATE_OBJECT.kind}
UPDATE_KWARGS = {"kind": SUITE_CREATE_OBJECT.kind}
DELETE_KWARGS = {"kind": SUITE_CREATE_OBJECT.kind}

print(f"{f" {SUITE_NAME} ":#^40}")
print(f"{SUITE_NAME} -> List")
for validate_method_list in [elem for elem in SUITE_TEST_CLASS.list(**LIST_KWARGS)]:
    print(f"\t \t -> : {validate_method_list.identifier}")

print(f"{SUITE_NAME} -> ScoreCards for Entity")
validation_object = SUITE_TEST_CLASS.get(identifier=SUITE_CREATE_OBJECT.identifier, **GET_KWARGS)
for entity_score in [
    elem for elem in SUITE_TEST_CLASS.get(identifier=SUITE_CREATE_OBJECT.identifier, **GET_KWARGS)
]:
    print(
        f"\t \t -> : {entity_score.identifier} has {entity_score.overall_score} across {len(entity_score.scorecard_scores)} scorecards"
    )

print(f"{SUITE_NAME} -> ScoreCard Summaries for Entity")
for score_summary in [
    elem
    for elem in client.scores.get_summary(identifier=SUITE_CREATE_OBJECT.identifier, **GET_KWARGS)
]:
    print(
        f"\t \t -> : {score_summary.identifier}.{score_summary.scorecard_identifier} = {score_summary.score}"
    )

print(f"Scores -> ScoreCard Recalibrate")
scores = client.scores.recalibrate(
    identifier=SUITE_CREATE_OBJECT.identifier,
    kind=SUITE_CREATE_OBJECT.kind,
    scorecard_identifier=global_idp_scorecard,
)
if scores:
    print(f"\t \t -> : {scores.identifier}.{scores.scorecard_identifier} = {scores.score}")
