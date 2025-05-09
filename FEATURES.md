# FEATURES

This document outlines the key features of the Luxury Teas e-commerce site, built using Django, Stripe, and Bootstrap.

---

## General

- Fully responsive design using Bootstrap 5
- Clear, consistent navigation bar:
  - Shop, Bag, Account links
  - Toasts appear to confirm user actions (e.g. login, logout, add to bag)
- Custom 404 error page
- Footer with social links and newsletter prompt

---

## Products and Shopping

- View all available loose-leaf teas with images, weights, and prices
- Product weights include: 30g, 100g, and 300g (prices scale accordingly)
- Add multiple items to the bag, with selected weights and quantities
- Edit weights and quantities directly in the bag
- Remove individual items
- Total and subtotal dynamically calculated
- Bag displays both regular teas and free samples (if added)

---

## Free Sample Logic

- If the user has not added all teas to their bag:
  - Up to 3 × 5g samples of missing teas are offered
- If the user has already added every tea:
  - A 20g sample of “Breakfast Blend” is offered instead
- Sample options are clearly shown in the bag
- Clicking a sample option adds it to the bag

---

## Checkout

- Secure Stripe integration for payments
- Users complete delivery details via a form
- Logged-in users can save delivery information to their profile
- Optional newsletter subscription checkbox appears at checkout (only if user is not already subscribed)
- On successful payment:
  - User is redirected to a confirmation page
  - Bag is cleared
  - Order is saved and visible in user’s profile

---

## User Accounts

- Register, log in, and log out using Django Allauth
- Navbar changes dynamically based on login status
- Profile page includes:
  - View/edit delivery details
  - View order history
  - Manage newsletter subscription
- Form is pre-filled with saved delivery info
- Access to “My Account” and profile management pages

---

## Newsletter Subscription

- Users can opt-in to email updates:
  - Via a checkbox at checkout (if not already subscribed)
  - Via the profile edit page
- If already subscribed:
  - The checkbox is replaced by an alert message at checkout
- Subscription state is stored in the `UserProfile` model (`subscribed_to_email`)
- Users can unsubscribe anytime from their profile page

---

## Blog (Superuser-Only Feature)

- Superusers can create, update, and delete blog posts
- Blog post list is shown on a dedicated admin panel
- Posts can be managed via buttons linked to the superuser dashboard

---

## Admin / Superuser Features

- Dedicated admin dashboard (/superuser/)
- View all orders from all users
- View and manage user enquiries
- Manage blog posts (CRUD)
- Regular users are denied access to this area

---

## Additional Features

- Responsive on all screen sizes (mobile, tablet, desktop)
- Validated HTML, CSS, JS and Python (W3C, JSHint, flake8)
- Fully documented testing and features
- Screenshot evidence provided in testing folder
