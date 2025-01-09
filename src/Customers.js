```jsx
import React, { useState } from 'react';

const CustomerManagement = () => {
  const [customers, setCustomers] = useState([]);
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');

  const addCustomer = () => {
    if (name && email) {
      setCustomers([...customers, { name, email }]);
      setName('');
      setEmail('');
    }
  };

  const removeCustomer = (index) => {
    const updatedCustomers = customers.filter((_, i) => i !== index);
    setCustomers(updatedCustomers);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    addCustomer();
  };

  return (
    <div>
      <h2>Customer Management System</h2>
      <form onSubmit={handleSubmit}>
        <input 
          type="text" 
          placeholder="Customer Name" 
          value={name} 
          onChange={(e) => setName(e.target.value)} 
        />
        <input 
          type="email" 
          placeholder="Customer Email" 
          value={email} 
          onChange={(e) => setEmail(e.target.value)} 
        />
        <button type="submit">Add Customer</button>
      </form>
      <ul>
        {customers.map((customer, index) => (
          <li key={index}>
            {customer.name} - {customer.email}
            <button onClick={() => removeCustomer(index)}>Remove</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default CustomerManagement;
```