=================================
How to apply for a job at agiliq
=================================

* Register yourself at http://join.agiliq.com/accounts/register/ and
  activate your account by following the link in the activation email.
* Login to your account with your email as your username and save the
  client id, client secret for future reference. Add a redirect uri
  where you will be redirected post the authorization and access token.
* Read the OAuth2_ spec or use an OAuth2 library (example: OAuthlib_) to
  authorize the application at http://join.agiliq.com/oauth/authorize/
* Exchange the authorization token for an access token at 
  http://join.agiliq.com/oauth/access_token/ . In this step, send the
  ``client_secret`` as an additional param (apart from the standard ones)
  while exchanging the authorization token for an access token.
* Using the access token make a multipart post request to 
  http://join.agiliq.com/api/resume/upload/ with the following form fields:

  * ``first_name``: Applicant's (your) first name
  * ``last_name``:  Applicant's (your) last name
  * ``projects_url``: Github/Bitbucket/any url where your projects reside
  * ``code_url``: The source code url where the code of how you authorized
    your app, exchanged the access token and the upload resides. Make sure
    to have a README with an optional link to your implementation.
  * ``resume``: Content of your resume (PDF, ODT, Doc or any other format)
    as a multipart upload.

In case you are stuck, feel free to check out ``application/tests.py``.

.. _OAuth2: http://tools.ietf.org/html/draft-ietf-oauth-v2
.. _OAuthlib: https://github.com/idan/oauthlib
