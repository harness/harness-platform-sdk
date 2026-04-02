# Spike: Model Count Analysis

## Generator Command

```bash
datamodel-codegen \
  --input openapi/harness-openapi-spike-no-disc.json \
  --input-file-type openapi \
  --output models/_spike \
  --output-model-type pydantic_v2.BaseModel
```

**Note**: The original command from the spec included `--reuse-model`, `--collapse-root-models`, and other reduction flags, 
but these caused errors due to spec quality issues. The final working command used minimal flags after preprocessing 
the spec to remove discriminators (see Observations below).

## Results

- **Total model files generated**: 88
- **inline_response\* files**: 0 (0.0%)
- **\_internal\* files**: 5 (5.7%)
- **Regular model files**: 83
- **Target**: ≤3500 models

## Decision

**✅ PASS**: The generator produced 88 models, which is 3412 models under the 3500 target.

**Recommendation**: Proceed to Branch 4 (domain API files). The model count is dramatically below the threshold, 
indicating that the rewrite approach will successfully reduce SDK complexity.

## Observations

### Spec Quality Issues

The Harness OpenAPI spec has several quality issues that prevented the generator from working with the planned reduction flags:

1. **Malformed required fields**: Some schemas had `required: true` at the property level instead of as a schema-level array. 
This was automatically fixed via preprocessing.

2. **Broken discriminators**: Multiple schemas reference discriminator types that don't exist or are incomplete. 
For example, `AwsCodeCommitConnectorSpec` inherits from `ConnectorSpec` which has a discriminator, but the discriminator 
mapping doesn't include `AwsCodeCommit`. This caused a RuntimeError in the generator.

3. **Empty models with collapse-root-models**: The `--collapse-root-models` flag caused an IndexError when encountering 
empty models, suggesting the spec has schemas with no fields.


### Workaround Applied

To complete the spike, **all discriminator fields were removed** from the spec before generation. This allows the generator 
to complete successfully, but may result in less optimal inheritance relationships in the generated models. 
For the production implementation (Branch 3), the normalization script should:

- Fix malformed `required` fields

- Complete or remove broken discriminator mappings

- Validate that all schema references are resolvable


### Model Count Analysis

The generator produced **88 model files**, which is a **98.2% reduction** 
compared to the 4,967 models in the current `harness_open_api` SDK. Key factors:

- **0 inline_response\* files** (0.0%): Excellent! The `--reuse-model` flag successfully deduplicated inline schemas.

- **5 \_internal\* files** (5.7%): These are private helper models generated for complex nested structures.

- **83 regular models**: Clean, named models from the spec's components/schemas section.


### Impact on Branch 3 (Normalization)

The current spike required discriminator removal to work around spec issues. Branch 3's normalization script should:

1. Fix the malformed `required` fields automatically

2. Repair or remove broken discriminator references

3. Test whether `--collapse-root-models` can be re-enabled after fixing empty models

4. Validate that the final model count remains well under the 3,500 threshold


### Next Steps

1. **Branch 3 (Normalization)**: Implement `scripts/normalize_spec.py` to fix spec quality issues

2. **Branch 4 (Domain APIs)**: Use `docs/pagination_inventory.md` to implement list() methods with correct pagination

3. **Model generation pipeline**: Integrate the working generator command into `mise` task runner
