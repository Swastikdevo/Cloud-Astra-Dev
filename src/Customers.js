```javascript
import React, { useState } from 'react';

const CustomerManagement = () => {
  const [customers, setCustomers] = useState([]);
  const [newCustomer, setNewCustomer] = useState({ name: '', email: '', phone: '' });

  const handleChange = (e) => {
    setNewCustomer({ ...newCustomer, [e.target.name]: e.target.value });
  };

  const handleAddCustomer = () => {
    setCustomers([...customers, newCustomer]);
    setNewCustomer({ name: '', email: '', phone: '' });
  };

  const handleDeleteCustomer = (index) => {
    const updatedCustomers = customers.filter((_, i) => i !== index);
    setCustomers(updatedCustomers);
  };

  return (
    <div>
      <h1>Customer Management System</h1>
      <input type="text" name="name" placeholder="Name" value={newCustomer.name} onChange={handleChange} />
      <input type="email" name="email" placeholder="Email" value={newCustomer.email} onChange={handleChange} />
      <input type="tel" name="phone" placeholder="Phone" value={newCustomer.phone} onChange={handleChange} />
      <button onClick={handleAddCustomer}>Add Customer</button>
      <ul>
        {customers.map((customer, index) => (
          <li key={index}>
            {customer.name} - {customer.email} - {customer.phone}
            <button onClick={() => handleDeleteCustomer(index)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default CustomerManagement;
```