```javascript
import React, { useState, useEffect } from 'react';

const CustomerList = () => {
  const [customers, setCustomers] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchCustomers = async () => {
      const response = await fetch('/api/customers');
      const data = await response.json();
      setCustomers(data);
      setLoading(false);
    };
    fetchCustomers();
  }, []);

  if (loading) return <div>Loading...</div>;

  return (
    <div>
      <h2>Customer List</h2>
      <ul>
        {customers.map(customer => (
          <li key={customer.id}>{customer.name}</li>
        ))}
      </ul>
    </div>
  );
};

const AddCustomerForm = ({ onAdd }) => {
  const [name, setName] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    onAdd({ name });
    setName('');
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        value={name}
        onChange={(e) => setName(e.target.value)}
        placeholder="Enter customer name"
      />
      <button type="submit">Add Customer</button>
    </form>
  );
};

const CustomerManagement = () => {
  const [customers, setCustomers] = useState([]);

  const addCustomer = (customer) => {
    setCustomers([...customers, { id: Date.now(), ...customer }]);
  };

  return (
    <div>
      <AddCustomerForm onAdd={addCustomer} />
      <CustomerList customers={customers} />
    </div>
  );
};

export default CustomerManagement;
```