# Blockchain Based Voting

A react client app built on top of balockchain based flask API. This app is built using redux and redux-toolkit for state management.

# Features

#### Block Explorer :

- Find block by index
- Find Transaction/Vote with Block by its ID
- Find list of Candidate's vote by candidate address

#### Authentication

Authenticate users using JWT tokens by accepting email and password

- SignIn
- SignOut
- SignUp

### Vote

- Create Vote: by uploading candidates name and number of voters, the system will generate PIN passwords for each voter and returns files to be downloaded.

- Cast Vote : select from the candidate and insert your PIN to cast your vote.

- Dashboard: to view all authenticated user's elections and thier results

- Vote Results: Display the election results for the general public

- As expected no update or delete is available

#### The blockchain API server for miners

- Block explorer
- Transaction and Block verification & Broadcasting
- Block mining
- p2p communication

## Available Scripts

### `yarn start`

Runs the app in the development mode.<br />
Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

### `yarn build`

Builds the app for production to the `build` folder.<br />

# Contribution

Any suggestion or contribution is welcome.
