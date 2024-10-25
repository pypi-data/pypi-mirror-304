'''
## CND Frameworks
**Easy access on CDN Frameworks for a clean environment**
Frameworks available
 - Bootstrap (v5.3.2)
 - Foundation (v6.6.3)
 - Materialize (v1.0.0)
 - Bulma (v0.9.4)
 - Semantic (v2.4.2)
 - Semantic UI (v2.4.2)
 - UIkit (v3.16.23)
 - Tailwind (v3.3.3)
 - Pure CSS (v2.1.0)
 - Spectre.css (v0.5.9)
 - Skeleton (v2.0.4)

### Usage:

### Flask App:

```python
from flask import Flask, render_template
from pipc_flask_app.framework import bootstrap_css, bootstrap_js, foundation_css, foundation_js, bulma_css 

@app.route('/')
def index():
    return render_template('your_page.html', 
                           bootstrap_css=bootstrap_css, 
                           bootstrap_js=bootstrap_js,
                           foundation_css=foundation_css,
                           foundation_js=foundation_js,
                           bulma_css=bulma_css)

if __name__ == '__main__':
    app.run(debug=True)
```

### Template:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flask App</title>
    
    <!-- Add your framework's CSS here -->
    {{ bootstrap_css|safe }}
    {{ foundation_css|safe }}
    {{ bulma_css|safe }}
    <!-- Add more frameworks as needed -->
</head>
<body>
    <!-- Add your page content here -->
    {% block content %}
    {% endblock %}

    <!-- Add your framework's JS here (optional) -->
    {{ bootstrap_js|safe }}
    {{ foundation_js|safe }}
    <!-- Add more frameworks' JS as needed -->
</body>
</html>
```

'''


# Bootstrap
bootstrap_css = '<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">'
bootstrap_js = '<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>'

# Foundation
foundation_css = '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/foundation-sites@6.6.3/dist/css/foundation.min.css">'
foundation_js = '<script src="https://cdn.jsdelivr.net/npm/foundation-sites@6.6.3/dist/js/foundation.min.js"></script>'

# Bulma
bulma_css = '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@0.9.4/css/bulma.min.css">'

# Tailwind CSS
tailwind_css = '<link href="https://cdn.jsdelivr.net/npm/tailwindcss@3.3.3/dist/tailwind.min.css" rel="stylesheet">'

# Materialize
materialize_css = '<link href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css" rel="stylesheet">'
materialize_js = '<script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/js/materialize.min.js"></script>'

# Semantic UI
semantic_ui_css = '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/semantic-ui@2.4.2/dist/semantic.min.css">'
semantic_ui_js = '<script src="https://cdn.jsdelivr.net/npm/semantic-ui@2.4.2/dist/semantic.min.js"></script>'

# UIkit
uikit_css = '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/uikit@3.16.23/dist/css/uikit.min.css">'
uikit_js = '<script src="https://cdn.jsdelivr.net/npm/uikit@3.16.23/dist/js/uikit.min.js"></script>'

# Pure CSS
pure_css = '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/purecss@2.1.0/build/pure-min.css">'

# Spectre.css
spectre_css = '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/spectre.css@0.5.9/dist/spectre.min.css">'

# Skeleton
skeleton_css = '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css">'

