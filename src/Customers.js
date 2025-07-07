```javascript
import React, { useState, useEffect } from 'react';

const CustomerDetails = ({ customerId }) => {
  const [customer, setCustomer] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchCustomer = async () => {
      setLoading(true);
      const response = await fetch(`/api/customers/${customerId}`);
      const data = await response.json();
      setCustomer(data);
      setLoading(false);
    };
    fetchCustomer();
  }, [customerId]);

  if (loading) return <div>Loading...</div>;

  return (
    <div>
      <h2>{customer.name}</h2>
      <p>Email: {customer.email}</p>
      <p>Phone: {customer.phone}</p>
      <p>Address: {customer.address}</p>
    </div>
  );
};

const CustomerManagement = () => {
  const [customers, setCustomers] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    const fetchCustomers = async () => {
      const response = await fetch('/api/customers');
      const data = await response.json();
      setCustomers(data);
    };
    fetchCustomers();
  }, []);

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
        onChange={e => setSearchTerm(e.target.value)} 
      />
      <ul>
        {filteredCustomers.map(customer => (
          <li key={customer.id}>
            <CustomerDetails customerId={customer.id} />
          </li>
        ))}
      </ul>
    </div>
  );
};

export default CustomerManagement;
```