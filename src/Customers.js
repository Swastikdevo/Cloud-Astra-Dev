```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
    const [customers, setCustomers] = useState([]);
    const [searchTerm, setSearchTerm] = useState('');
    const [sortOrder, setSortOrder] = useState('asc');

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

    const sortedCustomers = [...customers].sort((a, b) => {
        if (sortOrder === 'asc') {
            return a.name.localeCompare(b.name);
        }
        return b.name.localeCompare(a.name);
    });

    const filteredCustomers = sortedCustomers.filter(customer =>
        customer.name.toLowerCase().includes(searchTerm.toLowerCase())
    );

    return (
        <div>
            <h2>Customer Management</h2>
            <input
                type="text"
                placeholder="Search customers"
                value={searchTerm}
                onChange={handleSearch}
            />
            <button onClick={() => setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc')}>
                Sort: {sortOrder === 'asc' ? 'Ascending' : 'Descending'}
            </button>
            <ul>
                {filteredCustomers.map(customer => (
                    <li key={customer.id}>{customer.name} - {customer.email}</li>
                ))}
            </ul>
        </div>
    );
};

export default CustomerManagement;
```