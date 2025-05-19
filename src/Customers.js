```javascript
import React, { useState, useEffect } from 'react';

const CustomerForm = ({ onSubmit, customer }) => {
  const [name, setName] = useState(customer ? customer.name : '');
  const [email, setEmail] = useState(customer ? customer.email : '');
  
  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit({ name, email });
    setName('');
    setEmail('');
  };

  return (
    <form onSubmit={handleSubmit}>
      <input 
        type="text" 
        value={name} 
        onChange={(e) => setName(e.target.value)} 
        placeholder="Customer Name" 
        required 
      />
      <input 
        type="email" 
        value={email} 
        onChange={(e) => setEmail(e.target.value)} 
        placeholder="Customer Email" 
        required 
      />
      <button type="submit">Save Customer</button>
    </form>
  );
};

const CustomerList = ({ customers, onRemove }) => {
  return (
    <ul>
      {customers.map((customer, index) => (
        <li key={index}>
          {customer.name} - {customer.email} 
          <button onClick={() => onRemove(index)}>Delete</button>
        </li>
      ))}
    </ul>
  );
};

const CustomerManagement = () => {
  const [customers, setCustomers] = useState([]);
  
  const handleAddCustomer = (customer) => {
    setCustomers([...customers, customer]);
  };

  const handleRemoveCustomer = (index) => {
    const newCustomers = customers.filter((_, i) => i !== index);
    setCustomers(newCustomers);
  };

  return (
    <div>
      <h1>Customer Management</h1>
      <CustomerForm onSubmit={handleAddCustomer} />
      <CustomerList customers={customers} onRemove={handleRemoveCustomer} />
    </div>
  );
};

export default CustomerManagement;
```