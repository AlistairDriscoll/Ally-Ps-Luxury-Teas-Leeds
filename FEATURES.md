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

## Color Scheme

In going for a luxury tea company I did realise that a certain theme had to be made. Light pastel colours were used to make my website easy on the eye.

| Colour Description             | Value                        | Swatch |
|-------------------------------|------------------------------|--------|
| Primary Accent Orange         | `#f78e1e`                    | <div style="width:20px; height:20px; background:#f78e1e; border:1px solid #000;"></div> |
| Sample Hover Orange           | `#e47c00`                    | <div style="width:20px; height:20px; background:#e47c00; border:1px solid #000;"></div> |
| Button Orange (Secondary)     | `#e67e22`                    | <div style="width:20px; height:20px; background:#e67e22; border:1px solid #000;"></div> |
| Text Accent Orange            | `rgba(205, 102, 51, 1)`      | <div style="width:20px; height:20px; background:rgba(205,102,51,1); border:1px solid #000;"></div> |
| Soft Green Background         | `rgba(102, 205, 102, 0.4)`   | <div style="width:20px; height:20px; background:rgba(102,205,102,0.4); border:1px solid #000;"></div> |
| Stripe Base                   | `#ffffff`                    | <div style="width:20px; height:20px; background:#ffffff; border:1px solid #000;"></div> |
| Stripe Alt                    | `#fef7f1`                    | <div style="width:20px; height:20px; background:#fef7f1; border:1px solid #000;"></div> |
| Link Hover Blue               | `#0056b3`                    | <div style="width:20px; height:20px; background:#0056b3; border:1px solid #000;"></div> |
| General Black (text/borders) | `black`                      | <div style="width:20px; height:20px; background:black; border:1px solid #000;"></div> |
| Scrollbar Grey                | `#aaa`                       | <div style="width:20px; height:20px; background:#aaa; border:1px solid #000;"></div> |



## Products and Shopping

- View all available loose-leaf teas with images, weights, and prices
- Product weights include: 30g, 100g, and 300g (prices scale accordingly)
- Add multiple items to the bag, with selected weights and quantities
- Edit weights and quantities directly in the bag
- Remove individual items
- Total and subtotal dynamically calculated
- Bag displays both regular teas and free samples (if added)

![Shop card examples](documentation/features/shop.png)
![Product detail example](documentation/features/prod-detail.png)

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

#### Email subscription

I was first encouraged by my course to include an email marketing embedment from Mailchimp, but as a user can only buy from my website when they are signed up I deemed this at first not the right way to handle email marketing. I then made my own 'subscribed_to_email' variable in my UserProfile model and included my own HTML for this, but after encouragement from a tutor decided to also include a mailchimp newsletter subscription form. Instead of deleting my old functionality though I then turned it into a 'members_club' subscription where members with an account already can subscribe to get early offers on new teas amongst other perks (an idea I actually adopted from another tea company who invited me to do the same after I bought enough of their tea!)

![Members club subscription html](documentation/features/member_club.png)
Here is an example of the HTML showing when the user has subscribed already
![Footer](documentation/features/mailchimp-box.png) Then here is the footer including an email marketing form that both users and non users can subscribe to.
![Mailchimp subscribers](documentation/features/mailchimp-storage.png)
Here is a list of email subscribers that mailchimp store for you.
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
