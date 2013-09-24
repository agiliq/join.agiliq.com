.. image:: https://travis-ci.org/agiliq/join.agiliq.com.png?branch=master   :target: https://travis-ci.org/agiliq/join.agiliq.com        




.. image:: https://coveralls.io/repos/agiliq/join.agiliq.com/badge.png?branch=master  :target: https://coveralls.io/r/agiliq/join.agiliq.com?branch=master




=================================
How to apply for a job at agiliq
=================================

* Register yourself at http://join.agiliq.com/accounts/register/ and
  activate your account by following the link in the activation email.
* Login to your account with your email as your username and save the
  client id, client secret of the OAuth2 application for future reference.
  Add a redirect uri where you will be redirected post the authorization
  and access token.
* Read the OAuth2_ spec or the `Github OAuth flow`_ or use an OAuth2 library 
  (example: OAuthlib_) to authorize the application at 
  http://join.agiliq.com/oauth/authorize/
* Exchange the authorization token for an access token at 
  http://join.agiliq.com/oauth/access_token/ . In this step, send the
  ``client_secret`` as an additional param (apart from the standard ones)
  while exchanging the authorization token for an access token.
* Make a multipart post request to
  http://join.agiliq.com/api/resume/upload/?access_token=... with the
  following form fields:

  * ``first_name``: Applicant's (your) first name
  * ``last_name``:  Applicant's (your) last name
  * ``projects_url``: Github/Bitbucket/any url where your projects reside
  * ``code_url``: The source code url where the code of how you authorized
    this app, exchanged the access token and the resume upload resides. Make
    sure to have a README with an optional link to your implementation.
  * ``resume``: Content of your resume (PDF, ODT, Doc or any other format)
    as a multipart upload.

In case you are stuck, feel free to check out the ``application/tests.py``.

.. note::

    You are free to use any language, library or framework of your choice.

.. _OAuth2: http://tools.ietf.org/html/draft-ietf-oauth-v2
.. _OAuthlib: https://github.com/idan/oauthlib
.. _`Github OAuth flow`: http://developer.github.com/v3/oauth/#web-application-flow
