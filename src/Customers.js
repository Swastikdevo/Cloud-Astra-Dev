```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
  const [customers, setCustomers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    const fetchCustomers = async () => {
      const response = await fetch('/api/customers');
      const data = await response.json();
      setCustomers(data);
      setLoading(false);
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
      <h1>Customer Management</h1>
      <input
        type="text"
        placeholder="Search Customers"
        value={searchTerm}
        onChange={handleSearch}
      />
      {loading ? (
        <p>Loading...</p>
      ) : (
        <ul>
          {filteredCustomers.map(customer => (
            <li key={customer.id}>
              {customer.name} - {customer.email}
              <button onClick={() => console.log(`Edit ${customer.id}`)}>Edit</button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default CustomerManagement;
```