```javascript
import React, { useState, useEffect } from 'react';

const CustomerForm = ({ onSubmit }) => {
  const [customerData, setCustomerData] = useState({ name: '', email: '', phone: '' });
  const [errors, setErrors] = useState({});

  const validate = () => {
    const newErrors = {};
    if (!customerData.name) newErrors.name = 'Name is required';
    if (!customerData.email.includes('@')) newErrors.email = 'Valid email is required';
    if (!customerData.phone.match(/^\d+$/)) newErrors.phone = 'Phone must be numeric';
    return newErrors;
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setCustomerData({ ...customerData, [name]: value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const validationErrors = validate();
    if (Object.keys(validationErrors).length === 0) {
      onSubmit(customerData);
      setCustomerData({ name: '', email: '', phone: '' });
    } else {
      setErrors(validationErrors);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input type="text" name="name" value={customerData.name} onChange={handleChange} placeholder="Name" />
      {errors.name && <span>{errors.name}</span>}
      <input type="email" name="email" value={customerData.email} onChange={handleChange} placeholder="Email" />
      {errors.email && <span>{errors.email}</span>}
      <input type="text" name="phone" value={customerData.phone} onChange={handleChange} placeholder="Phone" />
      {errors.phone && <span>{errors.phone}</span>}
      <button type="submit">Add Customer</button>
    </form>
  );
};

const CustomerList = ({ customers }) => (
  <ul>
    {customers.map((customer, index) => (
      <li key={index}>{customer.name} - {customer.email} - {customer.phone}</li>
    ))}
  </ul>
);

const CustomerManagement = () => {
  const [customers, setCustomers] = useState([]);

  const addCustomer = (customer) => {
    setCustomers([...customers, customer]);
  };

  return (
    <div>
      <h1>Customer Management</h1>
      <CustomerForm onSubmit={addCustomer} />
      <CustomerList customers={customers} />
    </div>
  );
};

export default CustomerManagement;
```