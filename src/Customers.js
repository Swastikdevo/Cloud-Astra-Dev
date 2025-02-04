```javascript
import React, { useState, useEffect } from 'react';

const CustomerForm = ({ onAddCustomer }) => {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [address, setAddress] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (name && email) {
      onAddCustomer({ name, email, address });
      setName('');
      setEmail('');
      setAddress('');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input type="text" placeholder="Name" value={name} onChange={(e) => setName(e.target.value)} required />
      <input type="email" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} required />
      <input type="text" placeholder="Address" value={address} onChange={(e) => setAddress(e.target.value)} />
      <button type="submit">Add Customer</button>
    </form>
  );
};

const CustomerList = ({ customers }) => (
  <ul>
    {customers.map((customer, index) => (
      <li key={index}>
        {customer.name} - {customer.email} {customer.address && `(${customer.address})`}
      </li>
    ))}
  </ul>
);

const CustomerManagement = () => {
  const [customers, setCustomers] = useState([]);

  const handleAddCustomer = (customer) => {
    setCustomers((prev) => [...prev, customer]);
  };

  return (
    <div>
      <h1>Customer Management</h1>
      <CustomerForm onAddCustomer={handleAddCustomer} />
      <CustomerList customers={customers} />
    </div>
  );
};

export default CustomerManagement;
```