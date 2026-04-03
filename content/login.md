---
title: "Login"
date: 2026-03-16T16:35:00-07:00
layout: "login"
url: "/login"
---

Please log in to view protected content.

<div data-netlify-identity-button></div>

<hr style="margin: 2rem 0;">

### Request Access
If you've signed in but still can't see the content, you can request access here!

<form name="request-access" method="POST" data-netlify="true">
  <div style="margin-bottom: 1rem;">
    <label for="name" style="display: block; margin-bottom: 0.5rem;">Name:</label>
    <input type="text" id="name" name="name" required style="width: 100%; padding: 0.5rem; max-width: 400px;" />
  </div>
  <div style="margin-bottom: 1rem;">
    <label for="email" style="display: block; margin-bottom: 0.5rem;">Email (used to sign in):</label>
    <input type="email" id="email" name="email" required style="width: 100%; padding: 0.5rem; max-width: 400px;" />
  </div>
  <div style="margin-bottom: 1rem;">
    <label for="message" style="display: block; margin-bottom: 0.5rem;">Message:</label>
    <textarea id="message" name="message" required style="width: 100%; padding: 0.5rem; height: 100px; max-width: 400px;" placeholder="Say hi! For example: 'Hi JR - Remember me from the Relient K concert?'"></textarea>
  </div>
  <button type="submit" style="padding: 0.5rem 1rem; border-radius: 4px; border: 1px solid #ccc; cursor: pointer;">Request Access</button>
</form>
