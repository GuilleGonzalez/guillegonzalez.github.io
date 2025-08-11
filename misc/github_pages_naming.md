## How To Change the Default Website Title for Markdown GitHub Pages (Jekyll)  

To set a custom title for your GitHub Pages site, you need to define the title in both the markdown file's front matter and the `_config.yml`. Keep in mind that your GitHub repository cannot have a description.  

---

### Step 1: Add Title Metadata to the Markdown File  

At the top of the markdown file, insert the following front matter:  

```yaml
---
title: Example Title
---
```  

### Step 2: Set Title Metadata in `_config.yml`  

In the `_config.yml` file, include this line:  

```yaml
title: Example Title
```  

Replace `Example Title` with your desired title (spaces are allowed).  

---

### Key Title Components  

1. **ProjectName:** By default, this is the GitHub repository name. You can override it by setting the `title` property in `_config.yml`.  

2. **LabelName:** This is based on the markdown file's `title` metadata if it exists. If not specified, it defaults to the first `<h1>` or `<h2>` heading found on the page. If neither is present, `LabelName` will be excluded from the title.  

---

### Title Format Rules  

1. `{LabelName} | {ProjectName}`  
   - Used when `LabelName` is set and differs from `ProjectName`.  

2. `{ProjectName} | {repo_description}`  
   - Used when the GitHub repository has a description, and either no `LabelName` is defined or it matches `ProjectName`.  

3. `{ProjectName}`  
   - Used when the GitHub repository has no description, and no `LabelName` is defined or it matches `ProjectName`.  
   - This is also the only case where no website title will appear at the top of the web page.  

---

### Additional Notes  

- The page title is unaffected by regular content, commit messages, markdown metadata descriptions, or the `_config.yml` `description` property.
