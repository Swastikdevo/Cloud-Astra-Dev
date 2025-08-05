```javascript
import React, { useState, useEffect } from 'react';

const CustomerForm = ({ onAddCustomer }) => {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [age, setAge] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    const customer = { name, email, age };
    onAddCustomer(customer);
    setName('');
    setEmail('');
    setAge('');
  };

  return (
    <form onSubmit={handleSubmit}>
      <input value={name} onChange={(e) => setName(e.target.value)} placeholder="Name" required />
      <input value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Email" required type="email" />
      <input value={age} onChange={(e) => setAge(e.target.value)} placeholder="Age" required type="number" />
      <button type="submit">Add Customer</button>
    </form>
  );
};

const CustomerList = ({ customers }) => {
  return (
    <ul>
      {customers.map((customer, index) => (
        <li key={index}>{customer.name} - {customer.email} - {customer.age}</li>
      ))}
    </ul>
  );
};

const CustomerManagement = () => {
  const [customers, setCustomers] = useState([]);

  const addCustomer = (customer) => {
    setCustomers(prevCustomers => [...prevCustomers, customer]);
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