```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
  const [customers, setCustomers] = useState([]);
  const [query, setQuery] = useState('');
  
  useEffect(() => {
    fetchCustomers();
  }, []);
  
  const fetchCustomers = async () => {
    const response = await fetch('/api/customers');
    const data = await response.json();
    setCustomers(data);
  };

  const filteredCustomers = customers.filter(customer => 
    customer.name.toLowerCase().includes(query.toLowerCase())
  );

  const handleDelete = async (id) => {
    await fetch(`/api/customers/${id}`, { method: 'DELETE' });
    setCustomers(customers.filter(customer => customer.id !== id));
  };

  return (
    <div>
      <input 
        type="text" 
        placeholder="Search customers..." 
        value={query} 
        onChange={(e) => setQuery(e.target.value)} 
      />
      <ul>
        {filteredCustomers.map(customer => (
          <li key={customer.id}>
            {customer.name} 
            <button onClick={() => handleDelete(customer.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default CustomerManagement;
```