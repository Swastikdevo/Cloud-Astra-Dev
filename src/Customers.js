```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
  const [customers, setCustomers] = useState([]);
  const [formState, setFormState] = useState({ name: '', email: '' });
  
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
    setFormState({ ...formState, [name]: value });
  };
  
  const addCustomer = async (e) => {
    e.preventDefault();
    await fetch('/api/customers', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(formState),
    });
    setFormState({ name: '', email: '' });
    fetchCustomers();
  };

  const deleteCustomer = async (id) => {
    await fetch(`/api/customers/${id}`, { method: 'DELETE' });
    fetchCustomers();
  };

  return (
    <div>
      <h1>Customer Management</h1>
      <form onSubmit={addCustomer}>
        <input 
          type="text" 
          name="name" 
          value={formState.name} 
          onChange={handleInputChange} 
          placeholder="Customer Name" 
          required 
        />
        <input 
          type="email" 
          name="email" 
          value={formState.email} 
          onChange={handleInputChange} 
          placeholder="Customer Email" 
          required 
        />
        <button type="submit">Add Customer</button>
      </form>
      <ul>
        {customers.map(customer => (
          <li key={customer.id}>
            {customer.name} - {customer.email}
            <button onClick={() => deleteCustomer(customer.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default CustomerManagement;
```