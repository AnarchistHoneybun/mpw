# Directory structure
CONTENT_DIR = content
DEPLOY_DIR = deploy
TEMPLATE_DIR = templates
STYLE_DIR = styles

# Find all markdown files
INDEX_MD = $(CONTENT_DIR)/index.md
TOP_LEVEL_MD = $(CONTENT_DIR)/blog.md $(CONTENT_DIR)/projects.md
BLOG_POSTS = $(wildcard $(CONTENT_DIR)/blogpost/*.md)
PROJECT_POSTS = $(wildcard $(CONTENT_DIR)/projectpost/*.md)

# Convert source paths to destination paths
INDEX_HTML = $(DEPLOY_DIR)/index.html
TOP_LEVEL_HTML = $(patsubst $(CONTENT_DIR)/%.md,$(DEPLOY_DIR)/%.html,$(TOP_LEVEL_MD))
BLOG_HTML = $(patsubst $(CONTENT_DIR)/blogpost/%.md,$(DEPLOY_DIR)/blogpost/%.html,$(BLOG_POSTS))
PROJECT_HTML = $(patsubst $(CONTENT_DIR)/projectpost/%.md,$(DEPLOY_DIR)/projectpost/%.html,$(PROJECT_POSTS))

# All HTML files
ALL_HTML = $(INDEX_HTML) $(TOP_LEVEL_HTML) $(BLOG_HTML) $(PROJECT_HTML)

# Common pandoc options without CSS
PANDOC_OPTIONS = -s

# CSS paths for different levels
TOP_LEVEL_CSS = --css ../$(STYLE_DIR)/reset.css --css ../$(STYLE_DIR)/index.css
NESTED_CSS = --css ../../$(STYLE_DIR)/reset.css --css ../../$(STYLE_DIR)/index.css

# Default target
all: $(ALL_HTML)

# Create deploy directory structure
$(DEPLOY_DIR) $(DEPLOY_DIR)/blogpost $(DEPLOY_DIR)/projectpost:
	mkdir -p $@

# Build index page
$(INDEX_HTML): $(INDEX_MD) $(TEMPLATE_DIR)/home.html | $(DEPLOY_DIR)
	pandoc $(PANDOC_OPTIONS) $(TOP_LEVEL_CSS) --toc --template=$(TEMPLATE_DIR)/home.html -o $@ $<

# Build top-level pages
$(DEPLOY_DIR)/%.html: $(CONTENT_DIR)/%.md $(TEMPLATE_DIR)/top-level.html | $(DEPLOY_DIR)
	pandoc $(PANDOC_OPTIONS) $(TOP_LEVEL_CSS) --template=$(TEMPLATE_DIR)/top-level.html -o $@ $<

# Build blog posts
$(DEPLOY_DIR)/blogpost/%.html: $(CONTENT_DIR)/blogpost/%.md $(TEMPLATE_DIR)/page.html | $(DEPLOY_DIR)/blogpost
	pandoc $(PANDOC_OPTIONS) $(NESTED_CSS) --toc --template=$(TEMPLATE_DIR)/page.html -o $@ $<

# Build project posts
$(DEPLOY_DIR)/projectpost/%.html: $(CONTENT_DIR)/projectpost/%.md $(TEMPLATE_DIR)/page.html | $(DEPLOY_DIR)/projectpost
	pandoc $(PANDOC_OPTIONS) $(NESTED_CSS) --toc --template=$(TEMPLATE_DIR)/page.html -o $@ $<

# Clean
clean:
	rm -rf $(DEPLOY_DIR)

# Debug target to print variables
debug:
	@echo "Source markdown files:"
	@echo "Index: $(INDEX_MD)"
	@echo "Top-level: $(TOP_LEVEL_MD)"
	@echo "Blog posts: $(BLOG_POSTS)"
	@echo "Project posts: $(PROJECT_POSTS)"
	@echo "\nTarget HTML files:"
	@echo "Index: $(INDEX_HTML)"
	@echo "Top-level: $(TOP_LEVEL_HTML)"
	@echo "Blog posts: $(BLOG_HTML)"
	@echo "Project posts: $(PROJECT_HTML)"

.PHONY: all clean debug