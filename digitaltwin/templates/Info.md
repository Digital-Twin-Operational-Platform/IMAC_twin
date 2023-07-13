This folder contains the HTML files that will be compiled using FLASK. This example uses a constant "base" with site specific information being added within this framework via "block content".
"base.html" will contain the general visualisation of the site that will be used by all the pages. This would contain frames, banners, footers, and the bootstrap protocol.
The rest of the HTML files contain the site specific code, such as figures, descriptive text, input fields, etc. They all will start with
```
{% extends 'base.html' %}
{% block content %}
```
And end with
```
{% endblock %}
```

Within these blocks contains the HTML code for figures, divisions, tables, and all the other various visualisations.