```javascript
import React, { useState, useEffect } from 'react';

const CustomerList = () => {
    const [customers, setCustomers] = useState([]);
    const [searchTerm, setSearchTerm] = useState('');
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchCustomers = async () => {
            setLoading(true);
            const response = await fetch('/api/customers');
            const data = await response.json();
            setCustomers(data);
            setLoading(false);
        };
        fetchCustomers();
    }, []);

    const filteredCustomers = customers.filter(customer =>
        customer.name.toLowerCase().includes(searchTerm.toLowerCase())
    );

    return (
        <div>
            <input
                type="text"
                placeholder="Search Customers"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
            />
            {loading ? (
                <p>Loading...</p>
            ) : (
                <ul>
                    {filteredCustomers.map(customer => (
                        <li key={customer.id}>
                            {customer.name} - {customer.email}
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
};

export default CustomerList;
```