## Assumptions

For this task, several assumptions have been made to guide the development process:

1. **Loan Repayment**:

   - Funds received by the bank from users will be repaid with interest, similar to the loans provided to customers.
   - Both loans and funds from customers have a duration and interval for payment and receipt.

2. **Due Date**:

   - A due date is included in each operation, allowing the bank to set a deadline for repayment or receipt.

3. **Future Development**:
   - The system is designed with flexibility for future enhancements. For example, the Djoser create serializer has been extended to include `first_name` and `last_name`. In the future, additional user profile information may be stored, requiring further extension of the serializer.
   - A transaction model has been implemented to record transactions. This model can be extended to integrate with payment gateways such as Stripe or other gateways.
   - The installment model could be extended in the future to accommodate additional expenses in case of late payments by users.

---

# Accounts Domain

## Authentication and Authorization

To handle users, the API utilizes Djoser for authentication and authorization. The Djoser endpoints are utilized for user authentication and management.

### Customizations:

- **Custom User Serializer**: Extended Djoser with a custom user create serializer to make `first_name` and `last_name` required.

- **Permissions**:
  - `read_only`: Users have read-only permissions.
  - `is_staff`: Users with `is_staff` status have staff permissions.

### Endpoints:

- `auth/`: [Djoser Endpoints]
- `auth/add-staff`: Endpoint to promote a user to staff status. Only admins can add staff.

---

# Bank Domain

## Bank Model

- The Bank model includes attributes for `balance` and `date`, facilitating a log for all balance changes.

### Signals

- **Initial Bank Instance**: A post-migration signal is triggered to create the initial bank instance.
- **Initial Bank User Instance**: A post-migration signal is triggered to create a bank user admin with 'admin' as the username and password. This user is intended for use as a bank user in transactions.

## Loan Model

- The Loan model is designed to save loans, with a serializer extended to validate maximum balance amounts and ensure the minimum value is less than the maximum.

### Endpoints:

- `bank/loan`:
  - **POST**: Endpoint to add loans. Accessible only by staff.
  - **GET**: Endpoint to view loans. Accessible to all users.

---

# Operations Domain

## Operations Model

- The Operations model includes functions for obtaining installments and validating payment intervals.

### Endpoints:

- `operation/`: Endpoint to create and list operations.
- `operation/installment`: Endpoint to view installments.
- `operation/transaction`: Endpoint to view transactions only for the staff.
- `operation/pay`: Endpoint to pay for installments. (Requires `installment_id` as a query parameter)
- `operation/approve`: Endpoint to approve operations. (Requires `operation_id` as a query parameter)
