```javascript
import React, { useState, useEffect } from 'react';
import axios from 'axios';

const CustomerManagement = () => {
  const [customers, setCustomers] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchCustomers = async () => {
      const response = await axios.get('/api/customers');
      setCustomers(response.data);
      setLoading(false);
    };
    fetchCustomers();
  }, []);

  const filteredCustomers = customers.filter(customer =>
    customer.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const handleDelete = async (id) => {
    await axios.delete(`/api/customers/${id}`);
    setCustomers(customers.filter(customer => customer.id !== id));
  };

  if (loading) return <p>Loading...</p>;

  return (
    <div>
      <input
        type="text"
        placeholder="Search customers..."
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
      />
      <ul>
        {filteredCustomers.map(customer => (
          <li key={customer.id}>
            {customer.name} <button onClick={() => handleDelete(customer.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default CustomerManagement;
```