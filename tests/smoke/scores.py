import json

####################
# Scores Tests
####################
print(f"{' Scores ':#^40}")
# pipeline_identifier = "simple_test"
default_scope = client._default_scope
default_scope = Scope(
    account_id=client.account_id, org="Harness_Platform_Management", project="Solutions_Factory"
)
# print(f"Scores -> List")
# for list_scores in [
#     elem for elem in client.scores.list(kind="resource", scope=default_scope)
# ]:
#     print(f"\t \t -> : {list_scores.identifier} = {list_scores.overall_score}")

print(f"Scores -> ScoreCards for Entity")
for entity_score in [
    elem for elem in client.scores.get(identifier="lab", kind="resource", scope=default_scope)
]:
    print(f"\t \t -> : {entity_score.identifier} = {entity_score.overall_score}")

print(f"Scores -> ScoreCard Summaries for Entity")
for score_summary in [
    elem
    for elem in client.scores.get_summary(identifier="lab", kind="resource", scope=default_scope)
]:
    print(
        f"\t \t -> : {score_summary.identifier}.{score_summary.scorecard_identifier} = {score_summary.score}"
    )

print(f"Scores -> ScoreCard Recalibrate")
scores = client.scores.recalibrate(
    identifier="lab",
    kind="resource",
    scorecard_identifier="HSF_Resource_Scorecard",
    scope=default_scope,
)
if scores:
    print(f"\t \t -> : {scores.identifier}.{scores.scorecard_identifier} = {scores.score}")
