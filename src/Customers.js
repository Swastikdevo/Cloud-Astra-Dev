```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
  const [customers, setCustomers] = useState([]);
  const [formData, setFormData] = useState({ name: '', email: '' });

  useEffect(() => {
    fetchCustomers();
  }, []);

  const fetchCustomers = async () => {
    const response = await fetch('/api/customers');
    const data = await response.json();
    setCustomers(data);
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const addCustomer = async () => {
    const response = await fetch('/api/customers', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(formData),
    });
    if (response.ok) {
      fetchCustomers();
      setFormData({ name: '', email: '' });
    }
  };

  return (
    <div>
      <h2>Customer Management</h2>
      <form onSubmit={(e) => { e.preventDefault(); addCustomer(); }}>
        <input name="name" value={formData.name} onChange={handleInputChange} placeholder="Name" required />
        <input name="email" value={formData.email} onChange={handleInputChange} placeholder="Email" type="email" required />
        <button type="submit">Add Customer</button>
      </form>
      <ul>
        {customers.map((customer) => (
          <li key={customer.id}>{customer.name} - {customer.email}</li>
        ))}
      </ul>
    </div>
  );
};

export default CustomerManagement;
```