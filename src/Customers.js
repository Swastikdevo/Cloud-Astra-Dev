```javascript
import React, { useState, useEffect } from 'react';

const CustomerList = () => {
  const [customers, setCustomers] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchCustomers = async () => {
      const response = await fetch('/api/customers');
      const data = await response.json();
      setCustomers(data);
      setLoading(false);
    };
    fetchCustomers();
  }, []);

  if (loading) return <div>Loading...</div>;

  return (
    <div>
      <h1>Customer List</h1>
      <ul>
        {customers.map(customer => (
          <li key={customer.id}>{customer.name} - {customer.email}</li>
        ))}
      </ul>
    </div>
  );
};

const AddCustomer = ({ onAdd }) => {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');

  const handleSubmit = e => {
    e.preventDefault();
    onAdd({ name, email });
    setName('');
    setEmail('');
  };

  return (
    <form onSubmit={handleSubmit}>
      <input 
        type="text" 
        placeholder="Name" 
        value={name} 
        onChange={e => setName(e.target.value)} 
        required 
      />
      <input 
        type="email" 
        placeholder="Email" 
        value={email} 
        onChange={e => setEmail(e.target.value)} 
        required 
      />
      <button type="submit">Add Customer</button>
    </form>
  );
};

const CustomerManagement = () => {
  const [customers, setCustomers] = useState([]);

  const addCustomer = customer => {
    setCustomers(prev => [...prev, customer]);
  };

  return (
    <div>
      <AddCustomer onAdd={addCustomer} />
      <CustomerList customers={customers} />
    </div>
  );
};

export default CustomerManagement;
```