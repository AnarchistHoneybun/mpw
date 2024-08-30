# Directory variables
SRC_DIR := src
DEPLOY_DIR := deploy
TEMPLATE_DIR := templates
STYLE_DIR := styles
SCRIPT_DIR := scripts

# Find all Markdown files in the src directory
MD_FILES := $(wildcard $(SRC_DIR)/*.md)

# Generate a list of HTML files to be created in the deploy directory
HTML_FILES := $(patsubst $(SRC_DIR)/%.md,$(DEPLOY_DIR)/%.html,$(MD_FILES))

# Default target
all: $(HTML_FILES) copy_assets

# Rule to build HTML files from Markdown
$(DEPLOY_DIR)/%.html: $(SRC_DIR)/%.md $(TEMPLATE_DIR)/template.html Makefile
	@mkdir -p $(DEPLOY_DIR)
	pandoc --toc -s --css reset.css --css index.css -i $< -o $@ --template=$(TEMPLATE_DIR)/template.html

# Copy static assets to deploy directory
copy_assets:
	@mkdir -p $(DEPLOY_DIR)/css $(DEPLOY_DIR)/js
	cp $(STYLE_DIR)/*.css $(DEPLOY_DIR)/css/
	cp $(SCRIPT_DIR)/*.js $(DEPLOY_DIR)/js/

# Clean target
clean:
	rm -rf $(DEPLOY_DIR)

.PHONY: all copy_assets clean