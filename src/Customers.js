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
      <input type="text" value={name} onChange={(e) => setName(e.target.value)} placeholder="Name" required />
      <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Email" required />
      <input type="tel" value={phone} onChange={(e) => setPhone(e.target.value)} placeholder="Phone" required />
      <button type="submit">Add Customer</button>
    </form>
  );
};

const CustomerList = ({ customers }) => {
  return (
    <ul>
      {customers.map((customer, index) => (
        <li key={index}>{customer.name} - {customer.email} - {customer.phone}</li>
      ))}
    </ul>
  );
};

const CustomerManagement = () => {
  const [customers, setCustomers] = useState([]);

  const handleAddCustomer = (customer) => {
    setCustomers([...customers, customer]);
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