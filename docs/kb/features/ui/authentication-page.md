# Authentication Page

**Category**: Interface
**Related Projects**: [[db-chat-nl-master]]
**Technologies**: [[react]], [[typescript]], [[react-hooks]]
**Backend Features**: [[authentication]], [[jwt-bcrypt]]

---

## Overview

A full-page authentication interface for user login. The page features a branded logo, single sign-in form with email and password fields, and password visibility toggle. Registration is disabled in the current implementation.

**Key characteristics**:
- Full-page centered layout with brand identity
- Email and password input fields with validation
- Password visibility toggle (show/hide)
- Error message display for failed authentication
- Loading state during form submission
- Clean, minimal design focused on authentication task

---

## Layout Structure

### Visual Arrangement

```
┌──────────────────────────────────────────────────────┐
│                                                      │
│                                                      │
│              ┌─────────────────────┐                │
│              │                     │                │
│              │       ┌───┐         │                │
│              │       │IT │         │  ← Logo Circle │
│              │       └───┘         │                │
│              │                     │                │
│              │   Ipswich Town      │  ← Brand Name  │
│              │ Fan Data Insights   │  ← Subtitle    │
│              │                     │                │
│              ├─────────────────────┤                │
│              │                     │                │
│              │    Sign In          │  ← Form Title  │
│              │                     │                │
│              │  [Error message]    │  ← Error       │
│              │                     │                │
│              │  Email              │                │
│              │  ┌───────────────┐  │                │
│              │  │your@email.com │  │  ← Email Input │
│              │  └───────────────┘  │                │
│              │                     │                │
│              │  Password           │                │
│              │  ┌───────────────┐  │                │
│              │  │••••••••••  👁️ │  │  ← Password    │
│              │  └───────────────┘  │                │
│              │                     │                │
│              │  ┌───────────────┐  │                │
│              │  │   Sign In     │  │  ← Submit Btn  │
│              │  └───────────────┘  │                │
│              │                     │                │
│              └─────────────────────┘                │
│                                                      │
│                                                      │
└──────────────────────────────────────────────────────┘
```

**Components**:
- **Auth Page Container**: Full-page centered flex layout
- **Auth Container**: Card/box containing logo and form
- **Logo Section**: Circular logo, brand name, subtitle
- **Auth Form**: Sign in form with email, password, submit button
- **Error Message**: Red error banner at top of form
- **Form Groups**: Label + input field pairs
- **Password Toggle**: Eye icon button inside password field
- **Submit Button**: Primary action button to sign in

**Placement**: Full viewport, centered both horizontally and vertically

---

## Visual Elements

### Main Components

**Auth Page Container** (AuthPage.tsx:41):
- **Location**: Full viewport (100vw × 100vh)
- **Contains**: Auth container centered within
- **Purpose**: Provides centered, full-screen authentication layout
- **Visual style**: Neutral background (light gray or gradient), flex layout with center alignment

**Auth Container** (AuthPage.tsx:42-100):
- **Location**: Centered in page
- **Contains**: Logo section, auth form
- **Purpose**: Houses all authentication elements in bordered card
- **Visual style**: White background, rounded corners, subtle shadow, max-width 400-450px

**Logo Section** (AuthPage.tsx:43-47):
- **Location**: Top of auth container, above form
- **Contains**: Logo circle with "IT" text, "Ipswich Town" heading, "Fan Data Insights" subtitle
- **Purpose**: Brand identity and context
- **Visual style**:
  - Logo circle: Blue background, white "IT" text, circular shape (60-80px diameter)
  - Brand name (h1): Large, bold, dark text (20-24px)
  - Subtitle (p): Smaller, lighter gray text (14-16px)
  - Centered text alignment

**Auth Form** (AuthPage.tsx:49-100):
- **Location**: Below logo section within auth container
- **Contains**: Form title, error message, email input, password input, submit button
- **Purpose**: Collects credentials and submits to authentication API
- **Visual style**: Standard form layout, vertical stack, labels above inputs

**Form Title** (AuthPage.tsx:50):
- **Location**: Top of form
- **Contains**: Text "Sign In" (mode === 'login')
- **Purpose**: Indicates form purpose
- **Visual style**: h2, medium-large size (18-20px), centered or left-aligned

**Error Message** (AuthPage.tsx:52):
- **Location**: Below form title, above input fields (conditional)
- **Contains**: Error text (e.g., "Invalid credentials", "Authentication failed")
- **Purpose**: Displays authentication errors to user
- **Visual style**: Red background, white or dark text, padding, rounded corners, full-width

**Email Form Group** (AuthPage.tsx:54-65):
- **Location**: First input group in form
- **Contains**: "Email" label, email input field
- **Purpose**: Collects user email address
- **Visual style**:
  - Label: 12-14px, medium weight, above input
  - Input: Text field, placeholder "your@email.com", full-width, rounded border, padding
  - Type: email (browser validation)
  - Required: true
  - Disabled when isSubmitting: true

**Password Form Group** (AuthPage.tsx:67-89):
- **Location**: Second input group in form
- **Contains**: "Password" label, password input wrapper with field and toggle button
- **Purpose**: Collects password securely with optional visibility toggle
- **Visual style**:
  - Label: Same as email label
  - Input wrapper: Relative positioned container
  - Input: Password/text field (toggles based on showPassword), placeholder "Min 6 characters"
  - Toggle button: Eye emoji (👁️) or closed eye (🙈) icon, absolute positioned in right side of input
  - MinLength: 6 characters
  - Required: true
  - Disabled when isSubmitting: true

**Password Toggle Button** (AuthPage.tsx:80-88):
- **Location**: Inside password input field, right side
- **Contains**: Eye open emoji (👁️) or closed eye (🙈)
- **Purpose**: Toggle password visibility (text vs masked)
- **Visual style**:
  - Position: Absolute right inside input field
  - Background: Transparent or subtle
  - Cursor: Pointer
  - Tab index: -1 (skip in tab order)

**Submit Button** (AuthPage.tsx:91-97):
- **Location**: Bottom of form
- **Contains**: "Sign In" text (normal), "Please wait..." (loading)
- **Purpose**: Submit form to authenticate
- **Visual style**:
  - Primary button style (brand color background, white text)
  - Full-width
  - Padding: 12-16px vertical
  - Rounded corners
  - Disabled state: Grayed out when isSubmitting
  - Cursor: Pointer (enabled), not-allowed (disabled)

### Interactive Elements

**Email Input** (AuthPage.tsx:56-64):
- **Type**: Email (browser validation for format)
- **Placeholder**: "your@email.com"
- **Required**: Yes
- **Change**: Updates email state

**Password Input** (AuthPage.tsx:71-79):
- **Type**: Password (default) or Text (when showPassword is true)
- **Placeholder**: "Min 6 characters"
- **MinLength**: 6
- **Required**: Yes
- **Change**: Updates password state

**Password Toggle Button** (AuthPage.tsx:80-88):
- **Click**: Toggles showPassword state, changes input type and emoji
- **Tab index**: -1 (not in natural tab order)
- **Visual feedback**: Emoji changes (👁️ ↔ 🙈)

**Submit Button** (AuthPage.tsx:91-97):
- **Click**: Submits form, calls handleSubmit
- **Disabled**: When isSubmitting is true OR form is invalid
- **Visual feedback**: Loading text "Please wait...", disabled styling

**Form Submit** (AuthPage.tsx:20-36):
- **Submit event**: Prevents default, calls login() or register() based on mode
- **Success**: Redirects to main app (managed by useAuth hook)
- **Error**: Sets error state, displays error message, re-enables form

**User Actions**:
- **Type email**: Enter email address in email field
- **Type password**: Enter password in password field (masked by default)
- **Click password toggle**: Show/hide password as plain text
- **Press Enter in input**: Submit form (browser default)
- **Click "Sign In"**: Submit credentials, attempt login
- **See error**: Read error message, correct credentials, retry

**Visual States**:
- **Default**: Empty form, "Sign In" button enabled
- **Typing**: Fields populated, button enabled when both fields valid
- **Submitting**: Button shows "Please wait...", fields and button disabled, no error visible
- **Error**: Red error message appears, fields and button re-enabled
- **Success**: Form submits, user redirected (no visible state in this component)
- **Password visible**: Password field shows plain text, toggle shows 🙈
- **Password hidden**: Password field shows bullets (••••), toggle shows 👁️

---

## Responsive Behavior

**Desktop (>1024px)**:
- Auth container: 400-450px wide, centered horizontally and vertically
- Logo: Full size (70-80px circle)
- Form: Comfortable spacing and padding
- Inputs: Standard height (40-48px)

**Tablet (768-1024px)**:
- Auth container: 380-420px wide, still centered
- Logo: Slightly smaller (60-70px circle)
- Form: Maintains spacing
- Inputs: Same height

**Mobile (<768px)**:
- Auth container: Full-width with margins (320-360px max), vertically centered
- Logo: Smaller (50-60px circle)
- Form: Compressed spacing
- Inputs: Full-width, taller tap targets (48px minimum)
- Text sizes scale down slightly
- Error message may wrap or truncate

---

## User Flows

### Successful Login

1. User sees login page with empty form
2. User types email in email field
3. User types password in password field
4. User clicks "Sign In" button (or presses Enter)
5. Button shows "Please wait...", form disables
6. Backend validates credentials, returns JWT token
7. useAuth hook stores token, sets authenticated state
8. User redirected to main app (chat interface)

### Failed Login (Invalid Credentials)

1. User enters incorrect email or password
2. User clicks "Sign In"
3. Button shows "Please wait...", form disables
4. Backend returns error (401 Unauthorized)
5. Error state sets: "Invalid credentials" or custom message
6. Red error banner appears at top of form
7. Form re-enables, button returns to "Sign In"
8. User corrects credentials and retries

### Password Visibility Toggle

1. User types password, sees bullets (••••••)
2. User forgets what they typed or wants to verify
3. User clicks eye icon (👁️) on right side of password field
4. Password becomes visible as plain text
5. Icon changes to closed eye (🙈)
6. User verifies password, clicks icon again to hide
7. Password returns to bullets, icon returns to 👁️

### Form Validation Errors

1. User clicks "Sign In" with empty email field
2. Browser shows validation error: "Please fill out this field"
3. User enters email, leaves password empty
4. User clicks "Sign In"
5. Browser shows validation error on password field
6. User enters short password (4 characters)
7. Browser shows validation error: "Please lengthen this text to 6 characters or more"
8. User enters valid password (6+ chars), submits successfully

---

## Integration Points

**Backend Features Used**:
- [[authentication]] - Login endpoint validates credentials, returns JWT token
- [[jwt-bcrypt]] - Password hashed with bcrypt, JWT token generated for session

**Technologies**:
- [[react-hooks]] - useState for email, password, showPassword, error, isSubmitting states (AuthPage.tsx:12-16)
- [[react-hooks]] - useAuth hook provides login and register functions (AuthPage.tsx:18)
- [[typescript]] - Type-safe form events, auth mode enum (AuthPage.tsx:8, 20)

**Data Flow**:
- **Input**: User types email and password → setState updates
- **Submit**: handleSubmit prevents default → calls login(email, password) from useAuth
- **Auth**: useAuth hook sends POST to /api/auth/login → receives JWT token
- **Success**: Token stored in localStorage/state → isAuthenticated becomes true → app redirects
- **Error**: Catch block sets error state → error message displays in UI

---

## Component Hierarchy

```
AuthPage
└── AuthPageContainer (div)
    └── AuthContainer (div)
        ├── AuthLogo (div)
        │   ├── LogoCircle (div with "IT" text)
        │   ├── BrandName (h1)
        │   └── Subtitle (p)
        └── AuthForm (form)
            ├── FormTitle (h2)
            ├── ErrorMessage (div, conditional)
            ├── EmailFormGroup (div)
            │   ├── EmailLabel (label)
            │   └── EmailInput (input[type="email"])
            ├── PasswordFormGroup (div)
            │   ├── PasswordLabel (label)
            │   └── PasswordInputWrapper (div)
            │       ├── PasswordInput (input[type="password" or "text"])
            │       └── PasswordToggle (button with emoji)
            └── SubmitButton (button[type="submit"])
```

---

## Visual Design Patterns

**Color Usage**:
- Primary: Brand blue for logo background, submit button
- Background: Light gray or white for page, white for auth container
- Text: Dark gray/black for headings and labels, lighter gray for subtitle
- Error: Red background for error message, white or dark text
- Input borders: Light gray, darker on focus
- Button text: White on primary color

**Typography**:
- Brand name (h1): 20-24px, bold
- Subtitle: 14-16px, regular, gray
- Form title (h2): 18-20px, bold or semi-bold
- Labels: 12-14px, medium weight, uppercase or regular
- Input text: 14-16px, regular
- Error text: 13-14px, regular or medium
- Button text: 14-16px, medium weight, uppercase

**Spacing**:
- Logo section padding: 24-32px
- Form padding: 24-32px
- Input margin: 16px between form groups
- Label margin: 6-8px below label, above input
- Button margin: 20-24px top margin from last input
- Error message margin: 12-16px below title, above inputs

**Visual Effects**:
- Shadows: Subtle box-shadow on auth container (e.g., 0 4px 12px rgba(0,0,0,0.1))
- Borders: Light borders on inputs (1px), thicker or colored on focus
- Rounded corners: 8-12px on auth container, 4-6px on inputs and button
- Focus states: Blue outline or border on inputs and button
- Transitions: Smooth 150-200ms on hover and focus states
- Loading: Submit button may show subtle pulse or color shift during submission

---

## Accessibility

**Keyboard Navigation**:
- **Tab**: Navigate from email → password → toggle → submit button
- **Shift+Tab**: Reverse navigation
- **Enter**: Submit form from any input field
- **Space**: Activate password toggle or submit button when focused

**Screen Reader Support**:
- Logo: Alt text "Ipswich Town Fan Data Insights" or aria-label
- Labels: Associated with inputs via htmlFor attribute (AuthPage.tsx:55, 68)
- Error message: ARIA live region, announced when error appears
- Password toggle: ARIA label "Show password" or "Hide password"
- Submit button: Clear label "Sign In" or "Please wait..."
- Form: Implicit or explicit form label for context

**Focus Management**:
- Focus visible on all interactive elements (inputs, buttons)
- Focus order: Logo (skip) → Email → Password → Toggle (tab index -1, skip) → Submit
- Error state: Consider auto-focusing first invalid field
- Password toggle: Tab index -1 to skip, accessible via mouse only

---

## Code Snippets

**Implementation**: See [[language/snippets/react-auth-form.md]]

**Key patterns used**:
- **Controlled Form Pattern**: useState for all form fields, onChange handlers update state (AuthPage.tsx:12-14)
- **Async Submit Handler**: handleSubmit async function with try/catch for error handling (AuthPage.tsx:20-36)
- **Password Visibility Toggle**: useState for showPassword, changes input type and icon (AuthPage.tsx:14, 72, 80-88)
- **Loading State**: isSubmitting state disables form and changes button text during submission (AuthPage.tsx:16, 63, 78, 91-97)
- **Error Display**: Conditional rendering of error message when error state is truthy (AuthPage.tsx:52)
- **useAuth Hook**: Custom hook provides login and register functions, manages authentication state (AuthPage.tsx:18)

---

## Alternatives & Variations

**Similar UI Patterns**:
- **OAuth Social Login**: Add "Sign in with Google/GitHub" buttons (Pros: faster signup; Cons: third-party dependency)
- **Magic Link**: Email-based passwordless login (Pros: no password management; Cons: requires email access)
- **Multi-step Form**: Separate email and password screens (Pros: mobile-friendly; Cons: more clicks)
- **Split Login/Register**: Separate pages or two-column layout (Pros: clearer; Cons: more complex)
- **Modal Authentication**: Login in modal overlay instead of full page (Pros: keeps context; Cons: limited space)

**When to Use**:
- Use full-page when authentication is required before any app access
- Use modal when authentication is optional or mid-session (e.g., commenting)
- Use social login when user base expects it or signup friction is high
- Use magic link when targeting non-technical users who struggle with passwords
- Use multi-step when form is complex or mobile-first design

---

## Related

**UI Features**: [[chat-interface]], [[sidebar-navigation]], [[admin-panel]]
**Backend Features**: [[authentication]], [[jwt-bcrypt]]
**Technologies**: [[react]], [[typescript]], [[react-hooks]]
**Code Examples**: [[language/snippets/react-auth-form.md]]
**Projects Using This**: [[db-chat-nl-master]]

---

## Notes

- Registration UI exists in code but is disabled (mode hardcoded to 'login', signup button hidden) (AuthPage.tsx:11, 99)
- Password toggle uses emoji icons (👁️ 🙈) instead of SVG icons for simplicity (AuthPage.tsx:86)
- Password toggle button has tabIndex: -1 to skip in keyboard navigation (AuthPage.tsx:84)
- Form uses browser's native HTML5 validation (email format, required fields, minLength)
- useAuth hook manages authentication state, token storage, and redirects (not shown in this component)
- Error messages come from backend API or useAuth hook's catch block (AuthPage.tsx:32)
- Component assumes redirect happens elsewhere (useAuth or parent router) on successful login
- No "Forgot Password" link in current implementation
- No "Remember Me" checkbox in current implementation
- No rate limiting or CAPTCHA in UI (may exist in backend)
- Logo is placeholder with "IT" text, could be replaced with actual image logo
