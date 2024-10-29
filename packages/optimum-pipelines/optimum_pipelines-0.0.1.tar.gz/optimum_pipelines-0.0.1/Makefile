.PHONY: check test style generate

ROOTDIR:=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))

GENTOOLSDIR := $(ROOTDIR)/generation

foo:
	echo $(GENTOOLSDIR)

BUILDDIR ?= $(ROOTDIR)/build

GENBUILDDIR := $(BUILDDIR)/optimum/pipelines/generated
GENPKGDIR := $(ROOTDIR)/optimum/pipelines/generated

check_dirs := optimum test $(GENTOOLSDIR)

check:
	ruff check --show-fixes ${check_dirs}
	ruff format ${check_dirs} --diff

style:
	ruff check ${check_dirs} --fix
	ruff format ${check_dirs}

test:
	python -m pytest -sv test

clean:
	rm -rf $(BUILDDIR)
	rm -rf $(GENPKGDIR)
	rm -rf $(ROOTDIR)/build
	rm -rf $(ROOTDIR)/dist

ifndef SPECDIR
# If not specified on the command-line, fetch tasks specifications directory

SPECREV ?= 516ac0c429eeb4e972a09ed0be5892581fb12390
SPECDIR := $(BUILDDIR)/tasks

$(SPECDIR)/%/spec/input.json $(SPECDIR)/%/spec/output.json:
	install -d $(SPECDIR)
	curl -L https://github.com/huggingface/huggingface.js/archive/${SPECREV}.tar.gz --output $(SPECDIR)/sources.tar.gz
	tar -C $(SPECDIR) -xf $(SPECDIR)/sources.tar.gz --strip-components=5 huggingface.js-$(SPECREV)/packages/tasks/src/tasks
	# Use a relative path for schemas referencing common definitions
	find $(SPECDIR) \( -name input.json -o -name output.json \) -exec \
		python $(GENTOOLSDIR)/sedpy.py \
			{} \
			--pattern "/inference/schemas/common-definitions.json" \
			--substitution "../../common-definitions.json" \;
endif

# Helpers to return generated and spec files in the form:
# /gendir/snake_case_task/input|output.py
# /specdir/hyphenized-task/spec/input.json
snake_case = $(subst -,_,$(1))
gen_file = $(1)/$(call snake_case,$(2))/$(3).py
spec_file = $(SPECDIR)/$(1)/spec/$(2).json
gen_input = $(call gen_file,$(1),$(2),input)
spec_input = $(call spec_file,$(1),input)
gen_output = $(call gen_file,$(1),$(2),output)
spec_output = $(call spec_file,$(1),output)
gen_pipeline = $(call gen_file,$(1),$(2),pipeline)

# Helpers to generate task Makefile targets

#  Generate input.py/output.py for each task
define generate_io_file
	# $(1) Task input/output JSON schema file $(2) python output file
	install -d $(dir $(2))
	datamodel-codegen --input $(1) --input-file-type jsonschema --output $(2) --output-model-type pydantic_v2.BaseModel
endef

#  Generate pipeline class definition for each task
define generate_pipeline_file
	# $(1) task name $(2) python output file
	install -d $(dir $(2))
	python $(GENTOOLSDIR)/generate_pipeline.py $(1) -p $(BUILDDIR) -o $(2)
endef

# The list of supported tasks it maintained in a separate Makefile fragment
# that defines the TASKS variable
include $(GENTOOLSDIR)/tasks.mk

# Warning: the generation targets have an unusual structure.
# We put all targets for task generated files in a dynamically created Makefile fragment.
$(BUILDDIR)/tasks_targets.mk: Makefile $(GENTOOLSDIR)/tasks.mk
	@install -d $(BUILDDIR)
	@( $(foreach T,$(TASKS),\
		echo '$(call gen_input,$(GENBUILDDIR),$T): $(call spec_input,$T)';\
		echo '	$$(call generate_io_file, $$<, $$@)';\
		echo '$(call gen_output,$(GENBUILDDIR),$T): $(call spec_output,$T)';\
		echo '	$$(call generate_io_file, $$<, $$@)';\
		echo '$(call gen_pipeline,$(GENBUILDDIR),$T): $(call gen_input,$(GENBUILDDIR),$T) $(GENTOOLSDIR)/pipeline.jinja';\
		echo '	$$(call generate_pipeline_file, $T, $$@)';\
	) ) >$@

# make will (re)create the tasks_targets fragment Makefile if it does not exist or
# if the list of tasks is modified
-include $(BUILDDIR)/tasks_targets.mk

tasks_schema_files := $(foreach T,$(TASKS), $(call spec_input,$T) $(call spec_output,$T))
# Prevent make from removing schema files after generation
.SECONDARY: $(tasks_schema_files)
tasks_generated_files := $(foreach T,$(TASKS), $(call gen_input,$(GENPKGDIR),$T) \
                                               $(call gen_output,$(GENPKGDIR),$T) \
                                               $(call gen_pipeline,$(GENPKGDIR),$T))

$(GENPKGDIR)/__init__.py: $(GENTOOLSDIR)/init.jinja
	install -d $(dir $@)
	python $(GENTOOLSDIR)/generate_init.py $(TASKS) -o $@

$(GENPKGDIR)/%.py: $(GENBUILDDIR)/%.py
	install -d $(dir $@)
	cp $< $@

generated_files := $(GENPKGDIR)/__init__.py $(tasks_generated_files)

generate: $(generated_files) $(BUILDDIR)/tasks_targets.mk
	ruff check ${GENPKGDIR} --fix
	ruff format ${GENPKGDIR}
	@echo "Generation Done"

package: generate
	python -m build $(ROOTDIR)
