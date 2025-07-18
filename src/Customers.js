```javascript
import React, { useState, useEffect } from 'react';

const CustomerList = () => {
  const [customers, setCustomers] = useState([]);
  const [search, setSearch] = useState('');

  useEffect(() => {
    fetch('/api/customers')
      .then((res) => res.json())
      .then((data) => setCustomers(data))
      .catch((error) => console.error('Error fetching customers:', error));
  }, []);

  const filteredCustomers = customers.filter(customer =>
    customer.name.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div>
      <input
        type="text"
        placeholder="Search customers..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
      />
      <ul>
        {filteredCustomers.map(customer => (
          <li key={customer.id}>{customer.name} - {customer.email}</li>
        ))}
      </ul>
    </div>
  );
};

const AddCustomer = () => {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');

  const handleAddCustomer = (e) => {
    e.preventDefault();
    fetch('/api/customers', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, email }),
    }).then(() => {
      setName('');
      setEmail('');
      alert('Customer added successfully');
    });
  };

  return (
    <form onSubmit={handleAddCustomer}>
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
  );
};

const CustomerManagement = () => {
  return (
    <div>
      <h1>Customer Management System</h1>
      <AddCustomer />
      <CustomerList />
    </div>
  );
};

export default CustomerManagement;
```