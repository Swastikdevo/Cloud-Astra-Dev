```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
  const [customers, setCustomers] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCustomer, setSelectedCustomer] = useState(null);

  useEffect(() => {
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

  const handleSelectCustomer = (customer) => {
    setSelectedCustomer(customer);
  };

  return (
    <div>
      <input
        type="text"
        placeholder="Search customers"
        value={searchTerm}
        onChange={handleSearch}
      />
      <ul>
        {customers
          .filter(customer => customer.name.toLowerCase().includes(searchTerm.toLowerCase()))
          .map(customer => (
            <li key={customer.id} onClick={() => handleSelectCustomer(customer)}>
              {customer.name}
            </li>
          ))}
      </ul>
      {selectedCustomer && (
        <div>
          <h2>Details for {selectedCustomer.name}</h2>
          <p>Email: {selectedCustomer.email}</p>
          <p>Phone: {selectedCustomer.phone}</p>
        </div>
      )}
    </div>
  );
};

export default CustomerManagement;
```