```javascript
import React, { useState, useEffect } from 'react';

const CustomerForm = ({ onSubmit }) => {
  const [customer, setCustomer] = useState({ name: '', email: '', phone: '' });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setCustomer({ ...customer, [name]: value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(customer);
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

const CustomerList = ({ customers, onDelete }) => (
  <ul>
    {customers.map((customer, index) => (
      <li key={index}>
        {customer.name} - {customer.email} - {customer.phone}
        <button onClick={() => onDelete(index)}>Delete</button>
      </li>
    ))}
  </ul>
);

const CustomerManagement = () => {
  const [customers, setCustomers] = useState([]);

  const addCustomer = (customer) => {
    setCustomers([...customers, customer]);
  };

  const deleteCustomer = (index) => {
    setCustomers(customers.filter((_, i) => i !== index));
  };

  useEffect(() => {
    const savedCustomers = JSON.parse(localStorage.getItem('customers'));
    if (savedCustomers) setCustomers(savedCustomers);
  }, []);

  useEffect(() => {
    localStorage.setItem('customers', JSON.stringify(customers));
  }, [customers]);

  return (
    <div>
      <h1>Customer Management</h1>
      <CustomerForm onSubmit={addCustomer} />
      <CustomerList customers={customers} onDelete={deleteCustomer} />
    </div>
  );
};

export default CustomerManagement;
```