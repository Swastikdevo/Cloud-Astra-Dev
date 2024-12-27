```javascript
import React, { useState } from 'react';

const CustomerForm = ({ onAddCustomer }) => {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [phone, setPhone] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    onAddCustomer({ name, email, phone });
    setName('');
    setEmail('');
    setPhone('');
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        value={name}
        onChange={(e) => setName(e.target.value)}
        placeholder="Customer Name"
        required
      />
      <input
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="Customer Email"
        required
      />
      <input
        type="tel"
        value={phone}
        onChange={(e) => setPhone(e.target.value)}
        placeholder="Customer Phone"
        required
      />
      <button type="submit">Add Customer</button>
    </form>
  );
};

const CustomerList = ({ customers }) => {
  return (
    <ul>
      {customers.map((customer, index) => (
        <li key={index}>
          {customer.name} - {customer.email} - {customer.phone}
        </li>
      ))}
    </ul>
  );
};

const CustomerManagement = () => {
  const [customers, setCustomers] = useState([]);
  
  const addCustomer = (customer) => {
    setCustomers([...customers, customer]);
  };

  return (
    <div>
      <h1>Customer Management System</h1>
      <CustomerForm onAddCustomer={addCustomer} />
      <CustomerList customers={customers} />
    </div>
  );
};

export default CustomerManagement;
```