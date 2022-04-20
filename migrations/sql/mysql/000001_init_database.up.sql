CREATE TABLE group_x (
    id int not null AUTO_INCREMENT,
    uuid varchar(36) not null,
    name varchar(200) not null,
    PRIMARY KEY(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

CREATE unique INDEX groups_uuid_idx ON group_x(uuid);

CREATE TABLE users (
    id int not null AUTO_INCREMENT,
    uuid varchar(36) not null,
    email varchar(100) not null,
    PRIMARY KEY(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

CREATE unique INDEX users_uuid_idx ON users(uuid);

CREATE TABLE group_user_map (
    id int not null AUTO_INCREMENT,
    uuid varchar(36) not null,
    group_uuid varchar(36) not null DEFAULT '0000-00000-00000-0000',
    user_uuid varchar(36) not null DEFAULT '0000-00000-00000-0000',
    PRIMARY KEY(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

CREATE unique INDEX group_user_map_uuid_idx ON group_user_map(uuid);

CREATE TABLE roles (
    id int not null AUTO_INCREMENT,
    uuid varchar(36) not null,
    name varchar(200),
    description varchar(200),
    is_custom boolean,
    PRIMARY KEY(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

CREATE unique INDEX roles_uuid_idx ON roles(uuid);

CREATE TABLE gum_role_map (
    id int not null AUTO_INCREMENT,
    uuid varchar(36) not null,
    gum_uuid varchar(36) not null DEFAULT '0000-00000-00000-0000',
    role_uuid varchar(36) not null DEFAULT '0000-00000-00000-0000',
    PRIMARY KEY(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

CREATE unique INDEX gum_role_map_uuid_idx ON gum_role_map(uuid);

CREATE TABLE resources (
    id int not null AUTO_INCREMENT,
    uuid varchar(36) not null,
    type varchar(10),
    service_type varchar(100),
    service_name varchar(100),
    endpoint varchar(200),
    PRIMARY KEY(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

CREATE unique INDEX resources_uuid_idx ON resources(uuid);

CREATE TABLE permission (
    id int not null AUTO_INCREMENT,
    uuid varchar(36) not null,
    role_uuid varchar(36) not null DEFAULT '0000-00000-00000-0000',
    resource_uuid varchar(36) not null DEFAULT '0000-00000-00000-0000',
    action varchar(10),
    PRIMARY KEY(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

CREATE unique INDEX permission_uuid_idx ON permission(uuid);

CREATE TABLE projects (
    id int not null AUTO_INCREMENT,
    uuid varchar(36) not null,
    name varchar(100),
    description varchar(200),
    PRIMARY KEY(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

CREATE unique INDEX projects_uuid_idx ON projects(uuid);

CREATE TABLE user_project_map (
    id int not null AUTO_INCREMENT,
    uuid varchar(36) not null,
    user_uuid varchar(36) not null DEFAULT '0000-00000-00000-0000',
    project_uuid varchar(36) not null DEFAULT '0000-00000-00000-0000',
    PRIMARY KEY(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

CREATE unique INDEX user_project_map_uuid_idx ON user_project_map(uuid);

CREATE TABLE resource_mapping (
    id int not null AUTO_INCREMENT,
    uuid varchar(36) not null,
    resource_uuid varchar(36) not null DEFAULT '0000-00000-00000-0000',
    url varchar(200),
    PRIMARY KEY(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

CREATE unique INDEX resource_mapping_uuid_idx ON resource_mapping(uuid);

ALTER TABLE group_user_map ADD CONSTRAINT group_uuid_GUM_map_group_fk FOREIGN KEY (group_uuid) REFERENCES group_x(uuid) ON DELETE CASCADE;
ALTER TABLE group_user_map ADD CONSTRAINT user_uuid_GUM_map_group_fk FOREIGN KEY (user_uuid) REFERENCES users(uuid) ON DELETE CASCADE;
ALTER TABLE gum_role_map ADD CONSTRAINT gum_uuid_GUMRM_map_GUM_fk FOREIGN KEY (gum_uuid) REFERENCES group_user_map(uuid) ON DELETE CASCADE;
ALTER TABLE gum_role_map ADD CONSTRAINT role_uuid_GUMRM_map_role_fk FOREIGN KEY (role_uuid) REFERENCES roles(uuid) ON DELETE CASCADE;
ALTER TABLE permission ADD CONSTRAINT role_uuid_permissions_map_role_fk FOREIGN KEY (role_uuid) REFERENCES roles(uuid) ON DELETE CASCADE;
ALTER TABLE permission ADD CONSTRAINT resource_uuid_permissions_map_resource_fk FOREIGN KEY (resource_uuid) REFERENCES resources(uuid) ON DELETE CASCADE;
ALTER TABLE user_project_map ADD CONSTRAINT user_uuid_UPM_map_user_fk FOREIGN KEY (user_uuid) REFERENCES users(uuid) ON DELETE CASCADE;
ALTER TABLE user_project_map ADD CONSTRAINT project_uuid_UPM_map_project_fk FOREIGN KEY (project_uuid) REFERENCES projects(uuid) ON DELETE CASCADE;
ALTER TABLE resource_mapping ADD CONSTRAINT resource_mapping_resource_fk FOREIGN KEY (resource_uuid) REFERENCES resources(uuid) ON DELETE CASCADE;