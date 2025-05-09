# TESTING

This document outlines the testing performed for the site, including manual testing, validation tools, browser/device compatibility, and unresolved issues (if any).

---

## 1. Manual Testing

The following tests were performed manually to ensure expected functionality. Results are marked as 'Y' (pass) or 'N' (fail).

### User Authentication

| Category    | User Actions           | Expected Results | Y/N  | Comments    |
|-------------|------------------------|------------------|------|-------------|
| Sign up     | Click on Sign up/login link  | Taken to login page | Y | |
|             | Click on Signup page   | Taken to signup page | Y | |
|             | Fill in details on signup page | Email sent to user's address; confirmation message shown | Y | |
|             | Click confirmation link in email | Taken to email confirmation page | Y | |
|             | Click confirm email button | Account confirmed, taken to login page | Y | |
| Login       | Log in with username and password | User is signed in | Y | |
|             | Log in with email and password | User is signed in, navbar updates, toast appears | Y | |
| Logout      | Click logout link | Taken to logout confirmation page | Y | |
|             | Confirm logout | User is signed out, toast appears, redirected to shop | Y | |

### Shopping and Checkout

| Action | Expected Result | Y/N | Comments |
|--------|------------------|-----|----------|
| Add product to bag | Item appears in bag with correct weight and quantity | Y | |
| Edit item in bag | Weight and quantity update correctly | Y | |
| Delete item from bag | Item removed from bag | Y | |
| Qualify for free sample | Free tea sample added automatically | Y | |
| Checkout with valid Stripe card | Payment succeeds, success page shown | Y | |
| Save delivery info | Profile updates correctly if box is checked | Y | |
| Subscribe to email | Checkbox shown if not subscribed; value saved | Y | |
| Already subscribed user | Message shown instead of checkbox | Y | |
| Edit profile info | Updates successfully | Y | |
| Subscribe/unsubscribe via profile | Checkbox reflects current state | Y | |

---

## 2. Code Validation

| Tool        | Pages/Files Tested | Result |
|-------------|--------------------|--------|
| W3C HTML Validator | All template pages | Pass (minor warnings ignored for Django-specific tags) |
| W3C CSS Validator | Base CSS file | Pass |
| JSHint         | `checkout.js`, `bag.js`, `stripe.js` | Pass with `esversion: 6` set |
| flake8         | All Python files | Pass (after cleanup) |

---

## 3. Browser Compatibility

Site tested on:

| Browser      | Version | Result |
|--------------|---------|--------|
| Google Chrome | vXX | ✅ |
| Mozilla Firefox | vXX | ✅ |
| Safari (mobile) | iOS XX | ✅ |
| Microsoft Edge | vXX | ✅ |

Screenshots available in `/documentation/` folder.

---

## 4. Device Testing

Responsive behaviour tested using Chrome DevTools and real devices.

| Device | View | Result |
|--------|------|--------|
| Desktop (1920x1080) | All pages | ✅ |
| Tablet (768x1024) | Shop, Checkout, Bag | ✅ |
| Mobile (375x667) | Shop, Checkout, Blog | ✅ |

---

### 5. User Account Management

| Action | Expected Result | Y/N | Comments |
|--------|------------------|-----|----------|
| Access profile page | User sees their delivery info and order history | Y | |
| Edit delivery info from profile page | Form is pre-filled with saved data | Y | |
| Submit changes to delivery info | Updated info saved to `UserProfile` model | Y | Changes persist when reloading the page |
| Subscribe via profile | Checkbox saves user as subscribed | Y | |
| Unsubscribe via profile | Checkbox updates to false | Y | |
| Attempt to access another user's profile | User is redirected or shown error | Y | Security check confirmed |


### 6. Superuser Features (Blog / Admin Tools)

| Action | Expected Result | Y/N | Comments |
|--------|------------------|-----|----------|
| Access superuser dashboard (/superuser) | Superuser is shown admin panel | Y | Regular users cannot access this page |
| Create a blog post | Form appears; post is saved and visible on site | Y | |
| Edit a blog post | Edit form loads with correct data; updates saved | Y | |
| Delete a blog post | Post is removed from the site | Y | |
| View all orders | Admin can view all user orders | Y | |
| View all enquiries | Admin can read user-submitted enquiries | Y | |


## 7. Known Issues

- None encountered during testing.

---


