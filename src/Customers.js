```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
  const [customers, setCustomers] = useState([]);
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [editingIndex, setEditingIndex] = useState(-1);

  useEffect(() => {
    const fetchCustomers = async () => {
      const response = await fetch('/api/customers');
      const data = await response.json();
      setCustomers(data);
    };
    fetchCustomers();
  }, []);

  const handleAddOrUpdateCustomer = () => {
    if (editingIndex === -1) {
      setCustomers([...customers, { name, email }]);
    } else {
      const updatedCustomers = customers.map((customer, index) =>
        index === editingIndex ? { name, email } : customer
      );
      setCustomers(updatedCustomers);
    }
    resetForm();
  };

  const handleEditCustomer = (index) => {
    setEditingIndex(index);
    setName(customers[index].name);
    setEmail(customers[index].email);
  };

  const resetForm = () => {
    setName('');
    setEmail('');
    setEditingIndex(-1);
  };

  return (
    <div>
      <h1>Customer Management</h1>
      <form onSubmit={(e) => e.preventDefault()}>
        <input
          type="text"
          placeholder="Customer Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
        <input
          type="email"
          placeholder="Customer Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <button onClick={handleAddOrUpdateCustomer}>
          {editingIndex === -1 ? 'Add Customer' : 'Update Customer'}
        </button>
        <button onClick={resetForm}>Cancel</button>
      </form>
      <ul>
        {customers.map((customer, index) => (
          <li key={index}>
            {customer.name} - {customer.email}
            <button onClick={() => handleEditCustomer(index)}>Edit</button>
            <button onClick={() => setCustomers(customers.filter((_, i) => i !== index))}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default CustomerManagement;
```