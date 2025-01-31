```javascript
import React, { useState } from 'react';

const CustomerForm = ({ onAddCustomer }) => {
  const [customer, setCustomer] = useState({ name: '', email: '', phone: '' });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setCustomer({ ...customer, [name]: value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onAddCustomer(customer);
    setCustomer({ name: '', email: '', phone: '' });
  };

  return (
    <form onSubmit={handleSubmit}>
      <input type="text" name="name" value={customer.name} onChange={handleChange} placeholder="Name" required />
      <input type="email" name="email" value={customer.email} onChange={handleChange} placeholder="Email" required />
      <input type="tel" name="phone" value={customer.phone} onChange={handleChange} placeholder="Phone" required />
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

const CustomerManagementSystem = () => {
  const [customers, setCustomers] = useState([]);

  const handleAddCustomer = (newCustomer) => {
    setCustomers([...customers, newCustomer]);
  };

  return (
    <div>
      <h1>Customer Management System</h1>
      <CustomerForm onAddCustomer={handleAddCustomer} />
      <CustomerList customers={customers} />
    </div>
  );
};

export default CustomerManagementSystem;
```