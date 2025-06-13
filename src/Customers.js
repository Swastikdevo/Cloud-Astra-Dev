```javascript
import React, { useState, useEffect } from 'react';

const CustomerList = () => {
  const [customers, setCustomers] = useState([]);
  const [keyword, setKeyword] = useState('');

  useEffect(() => {
    const fetchCustomers = async () => {
      const response = await fetch('https://api.example.com/customers');
      const data = await response.json();
      setCustomers(data);
    };
    fetchCustomers();
  }, []);

  const filteredCustomers = customers.filter(customer => 
    customer.name.toLowerCase().includes(keyword.toLowerCase())
  );

  return (
    <div>
      <input 
        type="text" 
        placeholder="Search customer..." 
        value={keyword} 
        onChange={(e) => setKeyword(e.target.value)} 
      />
      <ul>
        {filteredCustomers.map(customer => (
          <li key={customer.id}>{customer.name}</li>
        ))}
      </ul>
    </div>
  );
};

export default CustomerList;
```