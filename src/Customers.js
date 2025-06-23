```javascript
import React, { useState } from 'react';

const CustomerForm = ({ onSubmit }) => {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [phone, setPhone] = useState('');
  
  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit({ name, email, phone });
    setName('');
    setEmail('');
    setPhone('');
  };

  return (
    <form onSubmit={handleSubmit}>
      <input 
        type="text" 
        placeholder="Name" 
        value={name} 
        onChange={(e) => setName(e.target.value)} 
      />
      <input 
        type="email" 
        placeholder="Email" 
        value={email} 
        onChange={(e) => setEmail(e.target.value)} 
      />
      <input 
        type="tel" 
        placeholder="Phone" 
        value={phone} 
        onChange={(e) => setPhone(e.target.value)} 
      />
      <button type="submit">Add Customer</button>
    </form>
  );
};

export const CustomerList = ({ customers }) => (
  <ul>
    {customers.map((customer, index) => (
      <li key={index}>
        {customer.name} - {customer.email} - {customer.phone}
      </li>
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