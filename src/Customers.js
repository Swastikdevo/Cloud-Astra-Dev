```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
  const [customers, setCustomers] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");
  
  useEffect(() => {
    // Simulating a fetch from an API
    const fetchCustomers = async () => {
      const response = await fetch('/api/customers');
      const data = await response.json();
      setCustomers(data);
    };
    fetchCustomers();
  }, []);
  
  const handleSearch = (e) => {
    setSearchTerm(e.target.value);
  };
  
  const filteredCustomers = customers.filter(customer =>
    customer.name.toLowerCase().includes(searchTerm.toLowerCase())
  );
  
  return (
    <div>
      <h2>Customer Management System</h2>
      <input 
        type="text" 
        placeholder="Search Customers..." 
        value={searchTerm} 
        onChange={handleSearch} 
      />
      <ul>
        {filteredCustomers.map(customer => (
          <li key={customer.id}>
            {customer.name} - {customer.email}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default CustomerManagement;
```