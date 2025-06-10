```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
  const [customers, setCustomers] = useState([]);
  const [filter, setFilter] = useState('');

  useEffect(() => {
    fetch('/api/customers')
      .then(res => res.json())
      .then(data => setCustomers(data));
  }, []);

  const filteredCustomers = customers.filter(customer => 
    customer.name.toLowerCase().includes(filter.toLowerCase())
  );

  const handleDelete = (id) => {
    fetch(`/api/customers/${id}`, { method: 'DELETE' })
      .then(() => setCustomers(customers.filter(customer => customer.id !== id)));
  };

  return (
    <div>
      <input 
        type="text" 
        placeholder="Search Customers" 
        value={filter} 
        onChange={(e) => setFilter(e.target.value)} 
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