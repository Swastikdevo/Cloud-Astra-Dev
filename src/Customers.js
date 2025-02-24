```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
  const [customers, setCustomers] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  
  useEffect(() => {
    fetchCustomers();
  }, []);
  
  const fetchCustomers = async () => {
    const response = await fetch('/api/customers');
    const data = await response.json();
    setCustomers(data);
  };

  const filteredCustomers = customers.filter(customer => 
    customer.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div>
      <input 
        type="text" 
        placeholder="Search Customers" 
        value={searchTerm} 
        onChange={(e) => setSearchTerm(e.target.value)} 
      />
      <ul>
        {filteredCustomers.map(customer => (
          <li key={customer.id}>{customer.name}</li>
        ))}
      </ul>
    </div>
  );
};

export default CustomerManagement;
```