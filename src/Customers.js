```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
  const [customers, setCustomers] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCustomer, setSelectedCustomer] = useState(null);

  useEffect(() => {
    fetchCustomers();
  }, []);

  const fetchCustomers = async () => {
    const response = await fetch('/api/customers');
    const data = await response.json();
    setCustomers(data);
  };

  const handleSearch = (e) => {
    setSearchTerm(e.target.value);
  };

  const handleSelectCustomer = (customer) => {
    setSelectedCustomer(customer);
  };

  const filteredCustomers = customers.filter(customer => 
    customer.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div>
      <input 
        type="text" 
        placeholder="Search customers..." 
        value={searchTerm} 
        onChange={handleSearch} 
      />
      <ul>
        {filteredCustomers.map(customer => (
          <li key={customer.id} onClick={() => handleSelectCustomer(customer)}>
            {customer.name}
          </li>
        ))}
      </ul>
      {selectedCustomer && (
        <div>
          <h2>{selectedCustomer.name}</h2>
          <p>Email: {selectedCustomer.email}</p>
          <p>Phone: {selectedCustomer.phone}</p>
        </div>
      )}
    </div>
  );
};

export default CustomerManagement;
```