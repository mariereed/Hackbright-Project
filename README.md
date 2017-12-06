# Blog Defog

Blog Defog is the media platform that your brain deserves. This simple and streamline RSS feed aggregator removes the stimulating and manipulative adds and styling commonly found on many blog and news sites. Articles are presented to the user fully sanitized, in a uniform calming format, all in one place. Blog Defog saves time, reduces mental load, and breaks the feedback loop for destructive habits.

## Tech Stack

Python Flask,
Flask SQLAlchemy,
JINJA2,
CSS,
HTML,
Bootstrap,
AJAX,
JSON,
Javascript,
JQuery

## APIs Used

Beautiful Soup:
  Used to sanitize content stripped from XML and to create text only sections
  
Schedule:
  Used to make requests every hour
  
Bcrypt:
  Used to hash passwords
  
Datetime:
  Used to compare publish dates and to timestamp

## Installation

Pip install -r requirements.txt

## Usage

Navigation:

  Cloud returns to homepage
  
  Avatar is a dropdown:
    Dashboard,
    Timeline,
    Logout
    
    
Homepage:

  Create new users,
  Login
  
  
From the dashboard:

  Unfavorite articles,
  Follow and unfollow blogs,
  Upload profile photo and custom background,
  
  
Timeline:

  Favorite and Hide articles,
  View articles
  
  
Article Page:

  Favorite and Hide articles,
  Back to timeline link returns to scrolled position

## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D

## Next Steps

I plan to create an RSS feed validator, which given a link will check to see if an RSS feed can be integrated with the current scraping algorithm. I will further develop the algorithm to allow for increased diversity in the XML formatting. And I plan to entirely prevent cross site scripting by only allowing whitelisted tags and attributes from blog content.
