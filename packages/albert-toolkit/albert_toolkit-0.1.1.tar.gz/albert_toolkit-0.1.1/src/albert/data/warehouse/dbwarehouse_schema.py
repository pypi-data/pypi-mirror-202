# coding: utf-8
from sqlalchemy import (
    CHAR,
    Column,
    DECIMAL,
    Date,
    DateTime,
    Enum,
    Float,
    Index,
    Integer,
    JSON,
    String,
    TIMESTAMP,
    Table,
    Text,
    text,
)
from sqlalchemy.dialects.mysql import LONGBLOB, LONGTEXT, MEDIUMTEXT, TINYINT, VARCHAR
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


t__casHazard = Table(
    "_casHazard",
    metadata,
    Column("casId", String(20), nullable=False),
    Column("name", String(255)),
    Column("snur", Integer),
    Column("coi", Integer),
    Column("tier2", Integer),
    Column("peroxide", Integer),
    Column("hap", Integer),
    Column("isProp65", Integer),
)


t__casSmiles = Table(
    "_casSmiles", metadata, Column("casNumber", String(200)), Column("smiles", Text)
)


class CountCol(Base):
    __tablename__ = "_countCol"

    parentId = Column(VARCHAR(20), primary_key=True, index=True)
    counter = Column(Integer)


class CountRow(Base):
    __tablename__ = "_countRow"

    parentId = Column(VARCHAR(20), primary_key=True, index=True)
    counter = Column(Integer)


t__inventoryHazardWGK = Table(
    "_inventoryHazardWGK",
    metadata,
    Column("albertId", String(20)),
    Column("calculatedHazard", Text),
    Column("WGK", Integer),
)


class Mapping(Base):
    __tablename__ = "_mapping"

    dynamoKey = Column(VARCHAR(100), primary_key=True)
    sqlTable = Column(VARCHAR(100))
    type = Column(VARCHAR(20))


t__report_table_definition = Table(
    "_report_table_definition",
    metadata,
    Column("Field", VARCHAR(100), nullable=False, server_default=text("''")),
    Column("Type", LONGTEXT, nullable=False),
    Column("reportType", VARCHAR(100), nullable=False, server_default=text("''")),
    Column("sequenceOrder", Integer),
)


class SequenceBatchColumn(Base):
    __tablename__ = "_sequenceBatchColumn"

    parentId = Column(VARCHAR(20), primary_key=True)
    sequence = Column(JSON)
    status = Column(String(20))
    createdAt = Column(TIMESTAMP)
    createdBy = Column(String(20), index=True)
    createdByName = Column(String(100))
    updatedAt = Column(TIMESTAMP)
    updatedBy = Column(String(20), index=True)
    updatedByName = Column(String(100))


class SequenceBatchRow(Base):
    __tablename__ = "_sequenceBatchRow"

    parentId = Column(VARCHAR(20), primary_key=True)
    sequence = Column(JSON)
    status = Column(String(20))
    createdAt = Column(TIMESTAMP)
    createdBy = Column(String(20), index=True)
    createdByName = Column(String(100))
    updatedAt = Column(TIMESTAMP)
    updatedBy = Column(String(20), index=True)
    updatedByName = Column(String(100))


class SequenceDesignColumn(Base):
    __tablename__ = "_sequenceDesignColumn"

    parentId = Column(VARCHAR(20), primary_key=True)
    sequence = Column(JSON)
    status = Column(String(20))
    createdAt = Column(TIMESTAMP)
    createdBy = Column(String(20), index=True)
    createdByName = Column(String(100))
    updatedAt = Column(TIMESTAMP)
    updatedBy = Column(String(20), index=True)
    updatedByName = Column(String(100))


class SequenceDesignRow(Base):
    __tablename__ = "_sequenceDesignRow"

    parentId = Column(VARCHAR(20), primary_key=True)
    sequence = Column(JSON)
    status = Column(String(20))
    createdAt = Column(TIMESTAMP)
    createdBy = Column(String(20), index=True)
    createdByName = Column(String(100))
    updatedAt = Column(TIMESTAMP)
    updatedBy = Column(String(20), index=True)
    updatedByName = Column(String(100))


class TimeDimension(Base):
    __tablename__ = "_timeDimension"
    __table_args__ = (Index("td_ymd_idx", "year", "month", "day", unique=True),)

    id = Column(Integer, primary_key=True)
    db_date = Column(Date, nullable=False, unique=True)
    year = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)
    day = Column(Integer, nullable=False)
    quarter = Column(Integer, nullable=False)
    week = Column(Integer, nullable=False)
    day_name = Column(String(9), nullable=False)
    month_name = Column(String(9), nullable=False)
    holiday_flag = Column(CHAR(1), server_default=text("'f'"))
    weekend_flag = Column(CHAR(1), server_default=text("'f'"))
    group_on = Column(String(50))


t__tmpDdbINVdetails_Symbols = Table(
    "_tmpDdbINVdetails_Symbols",
    metadata,
    Column("PK", String(50)),
    Column("SK", String(50)),
    Column("id", String(50)),
    Column("parentId", String(50)),
    Column("GS1PK", String(20)),
    Column("GS1SK", String(20)),
    Column("revisionDate", Date),
    Column("module", String(50)),
    Column("createdBy", String(50)),
    Column("unNumber", String(50)),
    Column("createdByName", MEDIUMTEXT),
    Column("createdAt", DateTime),
    Column("updatedBy", MEDIUMTEXT),
    Column("updatedAt", DateTime),
    Column("updatedByName", MEDIUMTEXT),
    Column("Symbols", JSON),
)


t__tmpDdbINVdetails_Symbols13Jan = Table(
    "_tmpDdbINVdetails_Symbols13Jan",
    metadata,
    Column("PK", String(50)),
    Column("SK", String(50)),
    Column("id", String(50)),
    Column("parentId", String(50)),
    Column("GS1PK", String(20)),
    Column("GS1SK", String(20)),
    Column("revisionDate", Date),
    Column("module", String(50)),
    Column("createdBy", String(50)),
    Column("unNumber", String(50)),
    Column("createdByName", MEDIUMTEXT),
    Column("createdAt", DateTime),
    Column("updatedBy", MEDIUMTEXT),
    Column("updatedAt", DateTime),
    Column("updatedByName", MEDIUMTEXT),
    Column("Symbols", JSON),
)


class TmpTaskConfig(Base):
    __tablename__ = "_tmpTaskConfig"

    dataColumnId = Column(VARCHAR(200), primary_key=True, nullable=False)
    defaultTaskName = Column(String(1000))
    hidden = Column(TINYINT(1))
    dataTemplateId = Column(VARCHAR(200), primary_key=True, nullable=False)
    target = Column(String(100))
    workflowId = Column(VARCHAR(200), primary_key=True, nullable=False)
    updatedAt = Column(TIMESTAMP)
    updatedByName = Column(String(1000))
    updatedBy = Column(String(200))


t__tmpTaskUsers_backfill = Table(
    "_tmpTaskUsers_backfill",
    metadata,
    Column("PK", String(25), nullable=False, server_default=text("''")),
    Column("SK", String(35), nullable=False, server_default=text("''")),
    Column("id", VARCHAR(20), nullable=False),
    Column("module", VARCHAR(3), nullable=False, server_default=text("''")),
    Column("dms", VARCHAR(4), nullable=False, server_default=text("''")),
    Column("category", VARCHAR(10), nullable=False, server_default=text("''")),
    Column("name", String(1000)),
    Column("GS1PK", String(25), nullable=False, server_default=text("''")),
    Column("GS1SK", VARCHAR(3), nullable=False, server_default=text("''")),
    Column("createdBy", String(20)),
    Column("createdByName", String(100)),
    Column("createdAt", TIMESTAMP),
    Column("updatedAt", TIMESTAMP),
    Column("updatedBy", String(20)),
    Column("updatedByName", String(100)),
)


t__tmp_dsteam = Table(
    "_tmp_dsteam",
    metadata,
    Column("oldDACName", String(200)),
    Column("oldDATName", String(200)),
    Column("DEV_DAC", String(20)),
    Column("DEV_DAT", String(20)),
    Column("PROD_DAC", String(20)),
    Column("PROD_DAT", String(20)),
)


t__tmp_dsteam_prodDC = Table(
    "_tmp_dsteam_prodDC",
    metadata,
    Column("id", String(20)),
    Column("name", String(200)),
)


t__tmp_dsteam_prodDT = Table(
    "_tmp_dsteam_prodDT",
    metadata,
    Column("id", String(20)),
    Column("name", String(200)),
)


t__tmpnewDBAccessProjectdetails = Table(
    "_tmpnewDBAccessProjectdetails",
    metadata,
    Column("userId", String(50)),
    Column("projectId", String(50)),
    Column("createdBy", String(50)),
    Column("createdAt", DateTime),
)


t__tmpworkflow25jan = Table(
    "_tmpworkflow25jan",
    metadata,
    Column("id", String(20), nullable=False),
    Column("name", String(1000)),
    Column("workflow", JSON),
    Column("workflowSequence", JSON),
    Column("workflowHash", String(50)),
    Column("status", String(20)),
    Column("createdAt", TIMESTAMP),
    Column("createdBy", String(20)),
    Column("createdByName", String(100)),
    Column("updatedAt", TIMESTAMP),
    Column("updatedBy", String(20)),
    Column("updatedByName", String(100)),
)


t__workflowParameter_18 = Table(
    "_workflowParameter_18",
    metadata,
    Column("id", VARCHAR(20)),
    Column("rowId", VARCHAR(10), nullable=False),
    Column("parentId", VARCHAR(20), nullable=False),
    Column("parentRowId", VARCHAR(20)),
    Column("name", String(100)),
    Column("value", VARCHAR(100)),
    Column("createdBy", String(20)),
    Column("createdByName", String(100)),
    Column("createdAt", TIMESTAMP),
    Column("updatedBy", String(20)),
    Column("updatedByName", String(100)),
    Column("updatedAt", TIMESTAMP),
)


t__workflow_18 = Table(
    "_workflow_18",
    metadata,
    Column("id", String(20), nullable=False),
    Column("name", String(1000)),
    Column("workflow", JSON),
    Column("workflowSequence", JSON),
    Column("workflowHash", String(50)),
    Column("status", String(20)),
    Column("createdAt", TIMESTAMP),
    Column("createdBy", String(20)),
    Column("createdByName", String(100)),
    Column("updatedAt", TIMESTAMP),
    Column("updatedBy", String(20)),
    Column("updatedByName", String(100)),
)


class AccessProject(Base):
    __tablename__ = "access_project"

    id = Column(VARCHAR(20), primary_key=True, nullable=False)
    parentId = Column(VARCHAR(20), primary_key=True, nullable=False, index=True)
    type = Column(String(10))
    createdBy = Column(String(20))
    createdAt = Column(TIMESTAMP)


class ActivityInventoryLot(Base):
    __tablename__ = "activity_inventoryLot"

    id = Column(String(20), primary_key=True, nullable=False)
    epochTime = Column(String(30), primary_key=True, nullable=False)
    startingInventory = Column(DECIMAL(30, 14))
    endingInventory = Column(DECIMAL(30, 14))
    inventoryType = Column(Enum("IT", "IA", "B", "PL", "P", "EXP"))
    inventoryNotes = Column(MEDIUMTEXT)
    salesOrderNo = Column(String(40))
    invoiceNo = Column(String(40))
    createdAt = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    createdBy = Column(String(20))
    createdByName = Column(String(100))
    updatedAt = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    updatedBy = Column(String(20))


class Attachment(Base):
    __tablename__ = "attachment"

    id = Column(String(20), primary_key=True)
    name = Column(String(1000))
    category = Column(String(50))
    fileSize = Column(Integer)
    Metadata = Column(JSON)
    revisionDate = Column(Date)
    key = Column(String(200))
    mimeType = Column(String(200))
    parentId = Column(String(50))
    status = Column(String(20))
    createdAt = Column(TIMESTAMP)
    createdBy = Column(String(20), index=True)
    createdByName = Column(String(100))
    updatedAt = Column(TIMESTAMP)
    updatedBy = Column(String(20), index=True)
    updatedByName = Column(String(100))


class BatchDataColumn(Base):
    __tablename__ = "batchDataColumn"

    id = Column(VARCHAR(20))
    batchTotal = Column(DECIMAL(30, 14))
    colId = Column(String(20), primary_key=True, nullable=False)
    designColId = Column(String(100))
    parentId = Column(VARCHAR(100), primary_key=True, nullable=False)
    productTotal = Column(DECIMAL(30, 14))
    referenceTotal = Column(DECIMAL(30, 14))
    type = Column(String(20))
    name = Column(String(1000))
    status = Column(String(20))
    createdAt = Column(TIMESTAMP)
    createdBy = Column(String(20), index=True)
    createdByName = Column(String(100))
    updatedAt = Column(TIMESTAMP)
    updatedBy = Column(String(20), index=True)
    updatedByName = Column(String(100))


class BatchDataColumnLot(Base):
    __tablename__ = "batchDataColumnLot"

    id = Column(VARCHAR(20))
    parentId = Column(VARCHAR(200), primary_key=True, nullable=False)
    colId = Column(String(20), primary_key=True, nullable=False)
    type = Column(String(20))
    name = Column(String(1000))
    createdAt = Column(TIMESTAMP)
    createdBy = Column(String(20), index=True)
    createdByName = Column(String(100))
    updatedAt = Column(TIMESTAMP)
    updatedBy = Column(String(20), index=True)
    updatedByName = Column(String(100))


class BatchDataRow(Base):
    __tablename__ = "batchDataRow"

    id = Column(VARCHAR(20))
    parentId = Column(String(200), primary_key=True, nullable=False)
    rowId = Column(VARCHAR(20), primary_key=True, nullable=False)
    designRowId = Column(VARCHAR(100))
    type = Column(String(20))
    name = Column(String(1000))
    parentRowId = Column(String(100))
    isLotParent = Column(TINYINT(1))
    status = Column(String(20))
    createdAt = Column(TIMESTAMP)
    createdBy = Column(String(20), index=True)
    createdByName = Column(String(100))
    updatedAt = Column(TIMESTAMP)
    updatedBy = Column(String(20), index=True)
    updatedByName = Column(String(100))


class BatchDataRowBkp1402(Base):
    __tablename__ = "batchDataRow_bkp_1402"

    id = Column(VARCHAR(20))
    parentId = Column(String(200), primary_key=True, nullable=False)
    rowId = Column(VARCHAR(20), primary_key=True, nullable=False)
    designRowId = Column(VARCHAR(100))
    type = Column(String(20))
    name = Column(String(1000))
    parentRowId = Column(String(100))
    isLotParent = Column(TINYINT(1))
    status = Column(String(20))
    createdAt = Column(TIMESTAMP)
    createdBy = Column(String(20), index=True)
    createdByName = Column(String(100))
    updatedAt = Column(TIMESTAMP)
    updatedBy = Column(String(20), index=True)
    updatedByName = Column(String(100))


class BatchDataValue(Base):
    __tablename__ = "batchDataValue"

    id = Column(VARCHAR(20))
    parentId = Column(VARCHAR(200), primary_key=True, nullable=False)
    batchValue = Column(DECIMAL(30, 14))
    productValue = Column(DECIMAL(30, 14))
    referenceValue = Column(DECIMAL(30, 14))
    colId = Column(String(20), primary_key=True, nullable=False)
    colParentId = Column(VARCHAR(100))
    colParentLotId = Column(String(200))
    rowId = Column(String(100), primary_key=True, nullable=False)
    rowParentId = Column(VARCHAR(100))
    designValId = Column(String(100))
    status = Column(String(20))
    createdAt = Column(TIMESTAMP)
    createdBy = Column(String(20), index=True)
    createdByName = Column(String(100))
    updatedAt = Column(TIMESTAMP)
    updatedBy = Column(String(20), index=True)
    updatedByName = Column(String(100))


class Ca(Base):
    __tablename__ = "cas"

    id = Column(String(20), primary_key=True)
    category = Column(String(100))
    description = Column(String(1000))
    casSmiles = Column(String(100))
    number = Column(VARCHAR(200))
    notes = Column(VARCHAR(200))
    status = Column(String(20))
    createdAt = Column(TIMESTAMP)
    createdBy = Column(String(20), index=True)
    createdByName = Column(String(100))
    updatedAt = Column(TIMESTAMP)
    updatedBy = Column(String(20), index=True)
    updatedByName = Column(String(100))


class Company(Base):
    __tablename__ = "company"

    id = Column(String(20), primary_key=True)
    name = Column(String(1000))
    status = Column(String(20))
    createdAt = Column(TIMESTAMP)
    createdBy = Column(String(20), index=True)
    createdByName = Column(String(100))
    updatedAt = Column(TIMESTAMP)
    updatedBy = Column(String(20), index=True)
    updatedByName = Column(String(100))


class CompanyBkp(Base):
    __tablename__ = "company_bkp"

    id = Column(String(20), primary_key=True)
    name = Column(String(1000))
    status = Column(String(20))
    createdAt = Column(TIMESTAMP)
    createdBy = Column(String(20), index=True)
    createdByName = Column(String(100))
    updatedAt = Column(TIMESTAMP)
    updatedBy = Column(String(20), index=True)
    updatedByName = Column(String(100))


class DataColumn(Base):
    __tablename__ = "dataColumn"

    id = Column(String(20), primary_key=True)
    default = Column(TINYINT(1))
    name = Column(String(1000))
    status = Column(String(20))
    createdAt = Column(TIMESTAMP)
    createdBy = Column(String(20), index=True)
    createdByName = Column(String(100))
    updatedAt = Column(TIMESTAMP)
    updatedBy = Column(String(20), index=True)
    updatedByName = Column(String(100))


class DataTemplate(Base):
    __tablename__ = "dataTemplate"

    id = Column(String(20), primary_key=True)
    name = Column(String(1000))
    _class = Column("class", String(50))
    status = Column(String(20))
    verified = Column(TINYINT(1))
    fullName = Column(String(500))
    description = Column(MEDIUMTEXT)
    Datacolumns = Column(JSON)
    Metadata = Column(JSON)
    createdAt = Column(TIMESTAMP)
    createdBy = Column(String(20), index=True)
    createdByName = Column(String(100))
    updatedAt = Column(TIMESTAMP)
    updatedBy = Column(String(20), index=True)
    updatedByName = Column(String(100))


class DataTemplateDataColumn(Base):
    __tablename__ = "dataTemplateDataColumn"
    __table_args__ = (Index("idx_parentId", "parentId", "id"),)

    id = Column(VARCHAR(20))
    parentId = Column(VARCHAR(20), primary_key=True, nullable=False)
    name = Column(String(100))
    calculation = Column(VARCHAR(1000))
    status = Column(String(100))
    value = Column(String(100))
    sequence = Column(VARCHAR(100), primary_key=True, nullable=False)
    hidden = Column(TINYINT(1))
    createdBy = Column(String(20))
    createdByName = Column(String(100))
    addedAt = Column(TIMESTAMP)
    createdAt = Column(TIMESTAMP)
    updatedBy = Column(String(20))
    updatedByName = Column(String(100))
    updatedAt = Column(TIMESTAMP)


class DataTemplateStandard(Base):
    __tablename__ = "dataTemplateStandard"

    id = Column(VARCHAR(20), primary_key=True, nullable=False)
    parentId = Column(VARCHAR(20), primary_key=True, nullable=False)
    standardId = Column(String(50), index=True)
    standardOrganization = Column(String(50))
    standardOrganizationId = Column(Integer)
    name = Column(VARCHAR(200))
    createdBy = Column(String(20))
    createdByName = Column(String(100))
    createdAt = Column(TIMESTAMP)
    updatedBy = Column(String(20))
    updatedByName = Column(String(100))
    updatedAt = Column(TIMESTAMP)


class DataTemplateTag(Base):
    __tablename__ = "dataTemplateTag"

    id = Column(String(20), primary_key=True, nullable=False)
    parentId = Column(String(20), primary_key=True, nullable=False)
    name = Column(String(100))
    createdBy = Column(String(20))
    createdAt = Column(TIMESTAMP)
    createdByName = Column(String(100))
    updatedBy = Column(String(20))
    updatedAt = Column(TIMESTAMP)
    updatedByName = Column(String(100))


class DataTemplateUnit(Base):
    __tablename__ = "dataTemplateUnit"

    id = Column(VARCHAR(20), nullable=False)
    parentId = Column(VARCHAR(20), primary_key=True, nullable=False)
    sequence = Column(VARCHAR(100), primary_key=True, nullable=False)
    name = Column(String(100))
    status = Column(String(100))
    symbol = Column(String(20))
    createdBy = Column(String(20))
    createdByName = Column(String(100))
    createdAt = Column(TIMESTAMP)
    updatedBy = Column(String(20))
    updatedByName = Column(String(100))
    updatedAt = Column(TIMESTAMP)


class Design(Base):
    __tablename__ = "design"
    __table_args__ = (Index("idx_parentId", "parentId", "id"),)

    id = Column(VARCHAR(20), primary_key=True)
    parentId = Column(String(20))
    type = Column(VARCHAR(20))
    status = Column(String(10))
    createdBy = Column(String(20))
    createdByName = Column(String(100))
    createdAt = Column(TIMESTAMP)
    updatedBy = Column(String(20))
    updatedByName = Column(String(100))
    updatedAt = Column(TIMESTAMP)


class DesignColumn(Base):
    __tablename__ = "designColumn"
    __table_args__ = (
        Index("idx_type_status", "type", "status"),
        Index("idx_parentId", "parentId", "colId"),
    )

    colId = Column(VARCHAR(10), primary_key=True, nullable=False)
    parentId = Column(String(20), primary_key=True, nullable=False)
    id = Column(VARCHAR(20))
    type = Column(String(10))
    name = Column(String(1000))
    status = Column(String(20))
    createdAt = Column(TIMESTAMP)
    createdBy = Column(String(20), index=True)
    createdByName = Column(String(100))
    updatedAt = Column(TIMESTAMP)
    updatedBy = Column(String(20), index=True)
    updatedByName = Column(String(100))


class DesignRow(Base):
    __tablename__ = "designRow"
    __table_args__ = (
        Index("idx_parentId", "parentId", "rowId"),
        Index("idx_type_status", "type", "status"),
    )

    rowId = Column(VARCHAR(10), primary_key=True, nullable=False)
    parentId = Column(String(20), primary_key=True, nullable=False)
    id = Column(VARCHAR(20))
    type = Column(String(10))
    name = Column(String(1000))
    status = Column(String(20))
    createdAt = Column(TIMESTAMP)
    createdBy = Column(String(20), index=True)
    createdByName = Column(String(100))
    updatedAt = Column(TIMESTAMP)
    updatedBy = Column(String(20), index=True)
    updatedByName = Column(String(100))


class DesignValue(Base):
    __tablename__ = "designValue"
    __table_args__ = (
        Index("idx_colInventoryId_rowType", "colInventoryId", "rowType"),
        Index("idx_parentId", "parentId", "rowId", "colId"),
        Index(
            "idx_rowInventoryId_rowType_createdAt",
            "rowInventoryId",
            "rowType",
            "createdAt",
        ),
        Index("idx_parentId_rowType", "parentId", "rowType"),
    )

    parentId = Column(VARCHAR(20), primary_key=True, nullable=False)
    rowId = Column(VARCHAR(10), primary_key=True, nullable=False)
    rowInventoryId = Column(String(20))
    rowType = Column(String(10))
    colId = Column(String(20), primary_key=True, nullable=False)
    colInventoryId = Column(String(20))
    value = Column(String(100))
    totalValue = Column(DECIMAL(30, 16))
    status = Column(String(20))
    createdAt = Column(TIMESTAMP)
    createdBy = Column(String(20), index=True)
    createdByName = Column(String(100))
    updatedAt = Column(TIMESTAMP)
    updatedBy = Column(String(20), index=True)
    updatedByName = Column(String(100))


class Inventory(Base):
    __tablename__ = "inventory"
    __table_args__ = (
        Index("idx_status_parentId", "status", "parentId"),
        Index("idx_parentId", "parentId", "status"),
        Index("idx_category_id", "category", "id", "status"),
    )

    id = Column(VARCHAR(20), primary_key=True)
    name = Column(VARCHAR(1000))
    description = Column(VARCHAR(1000))
    category = Column(String(20))
    validated = Column(TINYINT(1))
    inUse = Column(DECIMAL(30, 14))
    onHand = Column(DECIMAL(30, 14))
    status = Column(String(20))
    unit = Column(String(20))
    _class = Column("class", String(10))
    parentId = Column(String(100))
    Metadata = Column(JSON)
    createdAt = Column(TIMESTAMP)
    createdBy = Column(VARCHAR(20), index=True)
    createdByName = Column(VARCHAR(100))
    updatedAt = Column(TIMESTAMP)
    updatedBy = Column(String(20), index=True)
    updatedByName = Column(String(100))


class InventoryCas(Base):
    __tablename__ = "inventoryCas"

    id = Column(String(20), primary_key=True, nullable=False)
    parentId = Column(String(20), primary_key=True, nullable=False)
    parentName = Column(VARCHAR(1000))
    number = Column(VARCHAR(20))
    casSmiles = Column(String(100))
    min = Column(DECIMAL(30, 14))
    max = Column(DECIMAL(30, 14))
    createdAt = Column(TIMESTAMP)
    createdBy = Column(VARCHAR(20))
    createdByName = Column(VARCHAR(100))
    updatedAt = Column(TIMESTAMP)
    updatedBy = Column(String(20))
    updatedByName = Column(String(100))


class InventoryCompany(Base):
    __tablename__ = "inventoryCompany"

    id = Column(VARCHAR(20), primary_key=True, nullable=False)
    parentId = Column(VARCHAR(20), primary_key=True, nullable=False, index=True)
    name = Column(String(100))
    createdBy = Column(String(20))
    createdByName = Column(String(100))
    createdAt = Column(TIMESTAMP)
    updatedBy = Column(String(20))
    updatedByName = Column(String(100))
    updatedAt = Column(TIMESTAMP)


class InventoryList(Base):
    __tablename__ = "inventoryList"

    ID = Column(VARCHAR(20), primary_key=True, nullable=False)
    parentId = Column(VARCHAR(20), primary_key=True, nullable=False, index=True)
    name = Column(String(100))
    createdBy = Column(String(20))
    createdByName = Column(String(100))
    createdAt = Column(TIMESTAMP)
    updatedBy = Column(String(20))
    updatedByName = Column(String(100))
    updatedAt = Column(TIMESTAMP)


class InventoryLocation(Base):
    __tablename__ = "inventoryLocation"

    id = Column(String(20), primary_key=True, nullable=False)
    parentId = Column(String(20), primary_key=True, nullable=False)
    name = Column(String(100))
    minimum = Column(DECIMAL(30, 16))
    createdBy = Column(String(20))
    createdAt = Column(TIMESTAMP)
    createdByName = Column(String(100))
    updatedBy = Column(String(20))
    updatedAt = Column(TIMESTAMP)
    updatedByName = Column(String(100))


class InventoryLot(Base):
    __tablename__ = "inventoryLot"
    __table_args__ = (Index("idx_parentId", "parentId", "inventoryOnHand"),)

    id = Column(String(20), primary_key=True)
    parentId = Column(VARCHAR(20))
    barcodeId = Column(String(100))
    cost = Column(String(100))
    initialQuantity = Column(String(50))
    locationId = Column(String(20), index=True)
    locationName = Column(String(100))
    manufacturerLotNumber = Column(String(100))
    parentIdCategory = Column(String(20))
    parentName = Column(VARCHAR(1000))
    parentUnit = Column(String(20))
    sequence = Column(Integer)
    storageLocationId = Column(String(20), index=True)
    storageLocationName = Column(String(100))
    inventoryOnHand = Column(DECIMAL(30, 14))
    number = Column(String(100))
    expirationDate = Column(Date)
    Metadata = Column(JSON)
    packSize = Column(String(100))
    status = Column(String(20), index=True)
    createdAt = Column(TIMESTAMP)
    createdBy = Column(String(20), index=True)
    createdByName = Column(String(100))
    updatedAt = Column(TIMESTAMP)
    updatedBy = Column(String(20), index=True)
    updatedByName = Column(String(100))


class InventoryLotNumberInventoryHistory(Base):
    __tablename__ = "inventoryLotNumberInventoryHistory"

    inventoryLotNumberInventoryHistoryId = Column(Integer, primary_key=True)
    inventoryLotNumberLocationId = Column(Integer, index=True)
    startingInventory = Column(DECIMAL(30, 14))
    endingInventory = Column(DECIMAL(30, 14))
    inventoryType = Column(Enum("IT", "IA", "B", "PL", "P", "EXP"))
    inventoryNotes = Column(MEDIUMTEXT)
    salesOrderNo = Column(String(40))
    invoiceNo = Column(String(40))
    createdAt = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    createdBy = Column(Integer, index=True)
    updatedAt = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    updatedBy = Column(Integer, index=True)


class InventoryPricing(Base):
    __tablename__ = "inventoryPricing"

    id = Column(String(20), primary_key=True)
    currency = Column(String(100))
    default = Column(Integer)
    expirationDate = Column(Date)
    locationId = Column(String(20), index=True)
    locationName = Column(String(100))
    fob = Column(String(100))
    parentId = Column(String(20), index=True)
    unitCategory = Column(String(20))
    packSize = Column(String(20))
    companyId = Column(String(20), index=True)
    companyName = Column(String(100))
    price = Column(DECIMAL(30, 14))
    status = Column(String(20))
    createdAt = Column(TIMESTAMP)
    createdBy = Column(String(20), index=True)
    createdByName = Column(String(100))
    updatedAt = Column(TIMESTAMP)
    updatedBy = Column(String(20), index=True)
    updatedByName = Column(String(100))


class InventoryProperty(Base):
    __tablename__ = "inventoryProperty"

    parentId = Column(VARCHAR(20), primary_key=True)
    taskConfig = Column(JSON)
    validated = Column(Integer)
    createdAt = Column(TIMESTAMP)
    createdBy = Column(String(20))
    createdByName = Column(String(100))
    updatedAt = Column(TIMESTAMP)
    updatedBy = Column(String(20))
    updatedByName = Column(String(100))


class InventoryPropertyTarget(Base):
    __tablename__ = "inventoryPropertyTarget"

    parentId = Column(VARCHAR(20), primary_key=True, nullable=False)
    dataTemplateId = Column(VARCHAR(20), primary_key=True, nullable=False)
    workflowId = Column(VARCHAR(20), primary_key=True, nullable=False)
    dataColumnId = Column(VARCHAR(20), primary_key=True, nullable=False)
    defaultTaskName = Column(VARCHAR(1000), nullable=False)
    hidden = Column(String(10))
    target = Column(Text)


class InventoryRecentSD(Base):
    __tablename__ = "inventoryRecentSDS"
    __table_args__ = (Index("idx_parentId", "parentId", "id"),)

    id = Column(VARCHAR(20))
    parentId = Column(VARCHAR(20), primary_key=True)
    name = Column(String(100))
    revisionDate = Column(Date)
    Symbols = Column(JSON)
    unNumber = Column(String(10))
    createdBy = Column(String(20), index=True)
    createdByName = Column(String(100))
    createdAt = Column(TIMESTAMP)
    updatedBy = Column(String(20))
    updatedByName = Column(String(100))
    updatedAt = Column(TIMESTAMP)


class InventorySymbol(Base):
    __tablename__ = "inventorySymbols"
    __table_args__ = (Index("idx_parentId_status", "parentId", "status"),)

    id = Column(VARCHAR(20), primary_key=True, nullable=False)
    parentId = Column(String(100), primary_key=True, nullable=False)
    name = Column(VARCHAR(100))
    status = Column(VARCHAR(50), nullable=False)


class InventoryTag(Base):
    __tablename__ = "inventoryTag"

    id = Column(String(20), primary_key=True, nullable=False)
    parentId = Column(String(20), primary_key=True, nullable=False, index=True)
    name = Column(String(100))
    createdBy = Column(String(20))
    createdAt = Column(TIMESTAMP)
    createdByName = Column(String(100))
    updatedBy = Column(String(20))
    updatedAt = Column(TIMESTAMP)
    updatedByName = Column(String(100))


class LabBatchLotNumberInventoryHistory(Base):
    __tablename__ = "labBatchLotNumberInventoryHistory"

    labBatchLotNumberInventoryHistoryId = Column(Integer, primary_key=True)
    labBatchLotNumberLocationId = Column(Integer)
    startingInventory = Column(DECIMAL(30, 14))
    endingInventory = Column(DECIMAL(30, 14))
    inventoryType = Column(Enum("IT", "IA", "B", "PL", "P"))
    inventoryNotes = Column(MEDIUMTEXT)
    salesOrderNo = Column(String(40))
    invoiceNo = Column(String(40))
    createdAt = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    createdBy = Column(Integer, index=True)
    updatedAt = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    updatedBy = Column(Integer, index=True)


class List(Base):
    __tablename__ = "list"
    __table_args__ = (Index("idx_category_id", "category", "id"),)

    id = Column(String(20), primary_key=True)
    name = Column(String(1000))
    category = Column(String(20))
    status = Column(String(20))
    createdAt = Column(TIMESTAMP)
    createdBy = Column(String(20), index=True)
    createdByName = Column(String(100))
    updatedAt = Column(TIMESTAMP)
    updatedBy = Column(String(20), index=True)
    updatedByName = Column(String(100))


class Location(Base):
    __tablename__ = "location"

    id = Column(String(20), primary_key=True)
    name = Column(String(1000))
    address = Column(String(1000))
    country = Column(String(10))
    latitude = Column(DECIMAL(30, 16))
    longitude = Column(DECIMAL(30, 16))
    status = Column(String(20))
    createdAt = Column(TIMESTAMP)
    createdBy = Column(String(20), index=True)
    createdByName = Column(String(100))
    updatedAt = Column(TIMESTAMP)
    updatedBy = Column(String(20), index=True)
    updatedByName = Column(String(100))


class NoteAttachment(Base):
    __tablename__ = "noteAttachment"

    id = Column(VARCHAR(20), primary_key=True, nullable=False)
    parentId = Column(VARCHAR(20), primary_key=True, nullable=False, index=True)
    name = Column(String(100))
    key = Column(String(500))
    createdBy = Column(String(20))
    createdByName = Column(String(100))
    createdAt = Column(TIMESTAMP)
    updatedBy = Column(String(20))
    updatedByName = Column(String(100))
    updatedAt = Column(TIMESTAMP)


class Note(Base):
    __tablename__ = "notes"

    id = Column(String(20), primary_key=True)
    name = Column(String(1000))
    parentId = Column(String(100))
    status = Column(String(20))
    createdAt = Column(TIMESTAMP)
    createdBy = Column(String(20), index=True)
    createdByName = Column(String(100))
    updatedAt = Column(TIMESTAMP)
    updatedBy = Column(String(20), index=True)
    updatedByName = Column(String(100))


class Parameter(Base):
    __tablename__ = "parameter"

    id = Column(String(20), primary_key=True)
    name = Column(String(1000))
    category = Column(String(300))
    rank = Column(Integer)
    status = Column(String(20))
    createdAt = Column(TIMESTAMP)
    createdBy = Column(String(20), index=True)
    createdByName = Column(String(100))
    updatedAt = Column(TIMESTAMP)
    updatedBy = Column(String(20), index=True)
    updatedByName = Column(String(100))


class ParameterGroup(Base):
    __tablename__ = "parameterGroup"

    id = Column(String(20), primary_key=True)
    name = Column(String(1000))
    type = Column(String(50))
    verified = Column(TINYINT(1))
    parameters = Column(JSON)
    description = Column(MEDIUMTEXT)
    _class = Column("class", String(300))
    status = Column(String(20))
    createdAt = Column(TIMESTAMP)
    createdBy = Column(String(20), index=True)
    createdByName = Column(String(100))
    updatedAt = Column(TIMESTAMP)
    updatedBy = Column(String(20), index=True)
    updatedByName = Column(String(100))


class ParameterGroupParameter(Base):
    __tablename__ = "parameterGroupParameter"

    id = Column(VARCHAR(20))
    parentId = Column(VARCHAR(20), primary_key=True, nullable=False, index=True)
    name = Column(String(100))
    value = Column(String(1000))
    status = Column(String(100))
    category = Column(String(100))
    shortName = Column(String(100))
    sequence = Column(VARCHAR(100), primary_key=True, nullable=False)
    createdBy = Column(String(20))
    createdByName = Column(String(100))
    addedAt = Column(TIMESTAMP)
    createdAt = Column(TIMESTAMP)
    updatedBy = Column(String(20))
    updatedByName = Column(String(100))
    updatedAt = Column(TIMESTAMP)


class ParameterGroupParameterUnit(Base):
    __tablename__ = "parameterGroupParameterUnit"

    id = Column(VARCHAR(20), primary_key=True, nullable=False)
    parentId = Column(VARCHAR(20), primary_key=True, nullable=False, index=True)
    name = Column(String(1000))
    sequence = Column(String(100))
    createdBy = Column(String(20))
    createdByName = Column(String(100))
    createdAt = Column(TIMESTAMP)
    updatedBy = Column(String(20))
    updatedByName = Column(String(100))
    updatedAt = Column(TIMESTAMP)


class ParamterGroupDocument(Base):
    __tablename__ = "paramterGroupDocument"

    id = Column(VARCHAR(20), primary_key=True, nullable=False)
    parentId = Column(VARCHAR(20), primary_key=True, nullable=False, index=True)
    createdBy = Column(String(20))
    createdByName = Column(String(100))
    createdAt = Column(TIMESTAMP)
    updatedBy = Column(String(20))
    updatedByName = Column(String(100))
    updatedAt = Column(TIMESTAMP)


class ParamterGroupSpecialParameter(Base):
    __tablename__ = "paramterGroupSpecialParameter"

    id = Column(VARCHAR(20), primary_key=True, nullable=False)
    parentId = Column(VARCHAR(20), primary_key=True, nullable=False, index=True)
    name = Column(VARCHAR(1000))
    sequence = Column(String(100))
    status = Column(String(100))
    createdBy = Column(String(20))
    createdByName = Column(String(100))
    createdAt = Column(TIMESTAMP)
    updatedBy = Column(String(20))
    updatedByName = Column(String(100))
    updatedAt = Column(TIMESTAMP)


class Prediction(Base):
    __tablename__ = "prediction"

    id = Column(String(20), primary_key=True)
    name = Column(VARCHAR(500))
    dataColumnId = Column(String(100))
    dataColumnName = Column(String(100))
    dataColumnUniqueId = Column(String(100))
    dataTemplateId = Column(String(100))
    flaggingMetadata = Column(JSON)
    intervalId = Column(String(100))
    inventoryId = Column(String(100))
    logPrediction = Column(DECIMAL(20, 14))
    modelId = Column(String(100))
    modelName = Column(String(500))
    modelOrganization = Column(String(100))
    modelVersion = Column(String(50))
    normalizedPrediction = Column(DECIMAL(20, 14))
    normalizedStd = Column(DECIMAL(20, 14))
    normalizedStd_prediction = Column("normalizedStd/prediction", DECIMAL(20, 14))
    oneSigmaLower = Column(DECIMAL(20, 14))
    oneSigmaUpper = Column(DECIMAL(20, 14))
    parentId = Column(String(100))
    percentFormulaKnown = Column(Integer)
    predictionType = Column(String(100))
    projectId = Column(String(100))
    taskId = Column(String(100))
    userAverageDataPoint = Column(DECIMAL(20, 14))
    userStandardDeviation = Column(DECIMAL(20, 14))
    variable = Column(String(100))
    variableValue = Column(String(100))
    workflowId = Column(String(100))
    status = Column(String(20))
    createdAt = Column(TIMESTAMP)
    createdBy = Column(String(20), index=True)
    createdByName = Column(String(100))
    updatedAt = Column(TIMESTAMP)
    updatedBy = Column(String(20), index=True)
    updatedByName = Column(String(100))


class PredictionModel(Base):
    __tablename__ = "predictionModels"

    id = Column(String(200), primary_key=True, nullable=False)
    binlabels = Column(JSON)
    _class = Column("class", String(200))
    dataColumnId = Column(String(100))
    dataColumnName = Column(String(500))
    DataTemplates = Column(JSON)
    graduated = Column(TINYINT(1))
    hyperParameters = Column(JSON)
    logTransform = Column(TINYINT(1))
    mainEffectSensitivity = Column(JSON)
    modelEndpoint = Column(String(255))
    name = Column(String(255))
    organization = Column(String(200))
    rootMeanSquare = Column(JSON)
    status = Column(String(200))
    totalDatapoints = Column(Float(asdecimal=True))
    totalEffectSensitivity = Column(JSON)
    trainedInputsJSON = Column(JSON)
    unitDictionary = Column(JSON)
    version = Column(VARCHAR(200), primary_key=True, nullable=False)
    createdAt = Column(TIMESTAMP)


class Project(Base):
    __tablename__ = "project"

    id = Column(VARCHAR(20), primary_key=True)
    prefix = Column(VARCHAR(10))
    _class = Column("class", String(20))
    state = Column(String(20))
    appEngg = Column(JSON)
    Metadata = Column(JSON)
    description = Column(String(1000))
    status = Column(String(20))
    createdAt = Column(TIMESTAMP)
    createdBy = Column(VARCHAR(20), index=True)
    createdByName = Column(VARCHAR(100))
    updatedAt = Column(TIMESTAMP)
    updatedBy = Column(String(20), index=True)
    updatedByName = Column(String(100))


class ProjectList(Base):
    __tablename__ = "projectList"

    id = Column(VARCHAR(20), primary_key=True, nullable=False)
    parentId = Column(VARCHAR(20), primary_key=True, nullable=False)
    name = Column(String(100))
    createdBy = Column(String(20))
    createdByName = Column(String(100))
    createdAt = Column(TIMESTAMP)
    updatedBy = Column(String(20))
    updatedByName = Column(String(100))
    updatedAt = Column(TIMESTAMP)


class ProjectLocation(Base):
    __tablename__ = "projectLocation"

    id = Column(VARCHAR(20), primary_key=True, nullable=False)
    parentId = Column(VARCHAR(20), primary_key=True, nullable=False)
    name = Column(String(100))
    createdBy = Column(String(20))
    createdByName = Column(String(100))
    createdAt = Column(TIMESTAMP)
    updatedBy = Column(String(20))
    updatedByName = Column(String(100))
    updatedAt = Column(TIMESTAMP)


class ProjectProperty(Base):
    __tablename__ = "projectProperty"

    parentId = Column(VARCHAR(20), primary_key=True)
    taskConfig = Column(JSON)
    createdAt = Column(TIMESTAMP)
    createdBy = Column(String(20))
    createdByName = Column(String(100))
    updatedAt = Column(TIMESTAMP)
    updatedBy = Column(String(20))
    updatedByName = Column(String(100))


class ProjectPropertyTarget(Base):
    __tablename__ = "projectPropertyTarget"

    parentId = Column(String(20), primary_key=True, nullable=False)
    dataTemplateId = Column(String(20), primary_key=True, nullable=False)
    workflowId = Column(String(20), primary_key=True, nullable=False)
    defaultTaskName = Column(String(1000))
    hidden = Column(String(10))
    target = Column(Text)


class PropertyDatum(Base):
    __tablename__ = "propertyData"
    __table_args__ = (
        Index("idx_inv_value", "inventoryId", "value", "void", "hidden"),
        Index("idx_dataTemplateId_DC", "dataTemplateId", "dataColumnId"),
        Index("idx_dt_value", "dataTemplateId", "value", "void", "hidden"),
        Index("idx_dataColumnId", "dataColumnId", "value", "void", "hidden"),
        Index("idx_parentId", "parentId", "id"),
        Index("idx_dt_parentId", "dataTemplateId", "parentId", "inventoryId"),
    )

    id = Column(String(20), primary_key=True)
    parentId = Column(VARCHAR(20))
    value = Column(VARCHAR(500))
    inventoryId = Column(VARCHAR(20))
    category = Column(String(100))
    barcodeId = Column(String(100))
    lotId = Column(String(20))
    columnId = Column(String(10))
    dataColumnId = Column(String(20))
    dataColumnName = Column(String(100))
    dataColumnUniqueId = Column(String(100))
    dataTemplateFullName = Column(String(255))
    dataTemplateId = Column(String(20))
    dataTemplateName = Column(String(255))
    dtName = Column(String(255))
    finalWorkflow = Column(String(20))
    finalWorkflowName = Column(String(255))
    hidden = Column(TINYINT(1))
    initialWorkflow = Column(String(20))
    initialWorkflowName = Column(String(255))
    intervalRows = Column(String(20))
    taskId = Column(String(20))
    taskName = Column(String(255))
    trial = Column(Integer)
    void = Column(TINYINT(1))
    valueNumeric = Column(DECIMAL(30, 16))
    valueString = Column(String(1000))
    status = Column(VARCHAR(20))
    createdAt = Column(TIMESTAMP)
    createdBy = Column(VARCHAR(20), index=True)
    createdByName = Column(VARCHAR(100))
    updatedAt = Column(TIMESTAMP)
    updatedBy = Column(VARCHAR(20), index=True)
    updatedByName = Column(VARCHAR(100))


class Report(Base):
    __tablename__ = "report"

    id = Column(String(20), primary_key=True)
    name = Column(String(1000))
    inputData = Column(JSON)
    reportType = Column(String(1000))
    reportTypeId = Column(String(100))
    projectId = Column(String(255))
    status = Column(String(20))
    reportState = Column(LONGTEXT)
    createdAt = Column(TIMESTAMP)
    createdBy = Column(String(20), index=True)
    createdByName = Column(String(100))
    updatedAt = Column(TIMESTAMP)
    updatedBy = Column(String(20), index=True)
    updatedByName = Column(String(100))


class ReportType(Base):
    __tablename__ = "reportType"

    id = Column(String(20), primary_key=True)
    name = Column(String(1000))
    version = Column(Integer)
    _class = Column("class", String(200))
    componentInput = Column(JSON)
    spName = Column(String(1000))
    description = Column(MEDIUMTEXT)
    status = Column(String(20))
    createdAt = Column(TIMESTAMP)
    createdBy = Column(String(20), index=True)
    createdByName = Column(String(100))
    updatedAt = Column(TIMESTAMP)
    updatedBy = Column(String(20), index=True)
    updatedByName = Column(String(100))


class Standard(Base):
    __tablename__ = "standard"

    id = Column(String(20), primary_key=True)
    name = Column(String(1000))
    standardId = Column(String(300))
    standardOrganization = Column(String(255))
    standardOrganizationId = Column(Integer)
    status = Column(String(20))
    createdAt = Column(TIMESTAMP)
    createdBy = Column(String(20), index=True)
    createdByName = Column(String(100))
    updatedAt = Column(TIMESTAMP)
    updatedBy = Column(String(20), index=True)
    updatedByName = Column(String(100))


class StorageClas(Base):
    __tablename__ = "storageClass"

    id = Column(Integer, primary_key=True)
    storageClassNumber = Column(String(500), index=True)
    storageClassDescription = Column(Text)
    status = Column(VARCHAR(50))
    createdBy = Column(String(50))
    createdAt = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    updatedBy = Column(Integer)
    updatedAt = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))


class StorageCompatibility(Base):
    __tablename__ = "storageCompatibility"

    id = Column(Integer, primary_key=True)
    storageClassId1 = Column(Integer, index=True)
    storageClassId2 = Column(Integer, index=True)
    compatibilityOutput = Column(String(100))
    status = Column(String(50))
    createdBy = Column(Integer)
    createdAt = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    updatedBy = Column(Integer)
    updatedAt = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))


class StorageLocation(Base):
    __tablename__ = "storageLocation"

    id = Column(VARCHAR(20), primary_key=True, nullable=False)
    name = Column(VARCHAR(100))
    parentId = Column(VARCHAR(20), primary_key=True, nullable=False)
    parentName = Column(String(1000))
    status = Column(String(10))
    createdBy = Column(String(20))
    createdByName = Column(String(100))
    createdAt = Column(TIMESTAMP)
    updatedBy = Column(String(20))
    updatedByName = Column(String(100))
    updatedAt = Column(TIMESTAMP)


class Tag(Base):
    __tablename__ = "tag"

    id = Column(String(20), primary_key=True)
    name = Column(String(1000))
    status = Column(String(20))
    createdAt = Column(TIMESTAMP)
    createdBy = Column(String(20), index=True)
    createdByName = Column(String(100))
    updatedAt = Column(TIMESTAMP)
    updatedBy = Column(String(20), index=True)
    updatedByName = Column(String(100))


class Task(Base):
    __tablename__ = "task"
    __table_args__ = (Index("idx_category_status", "status", "category"),)

    id = Column(String(20), primary_key=True)
    parentId = Column(String(20))
    name = Column(String(1000))
    category = Column(String(20))
    dueDate = Column(DateTime)
    claimedDate = Column(DateTime)
    startDate = Column(DateTime)
    completedDate = Column(DateTime)
    closedDate = Column(DateTime)
    _class = Column("class", VARCHAR(20))
    priority = Column(VARCHAR(20))
    batchSizeUnit = Column(VARCHAR(20))
    state = Column(VARCHAR(20))
    status = Column(VARCHAR(20))
    createdAt = Column(TIMESTAMP)
    createdBy = Column(VARCHAR(20), index=True)
    createdByName = Column(VARCHAR(100))
    updatedAt = Column(TIMESTAMP)
    updatedBy = Column(VARCHAR(20), index=True)
    updatedByName = Column(VARCHAR(100))


class TaskAssignee(Base):
    __tablename__ = "taskAssignee"
    __table_args__ = (Index("idx_parentId", "parentId", "id"),)

    id = Column(VARCHAR(20), primary_key=True, nullable=False)
    parentId = Column(VARCHAR(20), primary_key=True, nullable=False)
    name = Column(String(100))
    category = Column(String(20))
    createdBy = Column(String(20))
    createdByName = Column(String(100))
    createdAt = Column(TIMESTAMP)
    updatedBy = Column(String(20))
    updatedByName = Column(String(100))
    updatedAt = Column(TIMESTAMP)


class TaskDataTemplate(Base):
    __tablename__ = "taskDataTemplate"
    __table_args__ = (Index("idx_parentId", "parentId", "id"),)

    id = Column(VARCHAR(20))
    parentId = Column(VARCHAR(20), primary_key=True)
    name = Column(String(100))
    createdBy = Column(String(20))
    createdByName = Column(String(100))
    createdAt = Column(TIMESTAMP)
    updatedBy = Column(String(20))
    updatedByName = Column(String(100))
    updatedAt = Column(TIMESTAMP)


class TaskInventoryLot(Base):
    __tablename__ = "taskInventoryLot"
    __table_args__ = (Index("idx_parentId", "parentId", "id"),)

    id = Column(VARCHAR(20), primary_key=True, nullable=False)
    parentId = Column(VARCHAR(20), primary_key=True, nullable=False)
    batchSize = Column(DECIMAL(30, 14))
    lotId = Column(VARCHAR(50))
    name = Column(VARCHAR(1000))
    lotNumber = Column(VARCHAR(20))
    barcodeId = Column(VARCHAR(50))
    category = Column(String(50))
    invLotUniqueId = Column(VARCHAR(100))
    createdBy = Column(String(20))
    createdByName = Column(String(100))
    createdAt = Column(TIMESTAMP)
    updatedBy = Column(String(20))
    updatedByName = Column(String(100))
    updatedAt = Column(TIMESTAMP)


class TaskLocation(Base):
    __tablename__ = "taskLocation"
    __table_args__ = (Index("idx_parentId_id", "parentId", "id"),)

    id = Column(VARCHAR(20), primary_key=True, nullable=False)
    parentId = Column(VARCHAR(20), primary_key=True, nullable=False)
    name = Column(String(100))
    createdBy = Column(String(20))
    createdByName = Column(String(100))
    createdAt = Column(TIMESTAMP)
    updatedBy = Column(String(20))
    updatedByName = Column(String(100))
    updatedAt = Column(TIMESTAMP)


class TaskTag(Base):
    __tablename__ = "taskTag"

    id = Column(VARCHAR(20), primary_key=True, nullable=False)
    parentId = Column(VARCHAR(20), primary_key=True, nullable=False, index=True)
    name = Column(String(100))
    createdBy = Column(String(20))
    createdByName = Column(String(100))
    createdAt = Column(TIMESTAMP)
    updatedBy = Column(String(20))
    updatedByName = Column(String(100))
    updatedAt = Column(TIMESTAMP)


class TaskWorkflow(Base):
    __tablename__ = "taskWorkflow"
    __table_args__ = (Index("idx_parentId", "parentId", "id"),)

    id = Column(VARCHAR(20), index=True)
    parentId = Column(VARCHAR(20), primary_key=True, nullable=False)
    category = Column(VARCHAR(10), primary_key=True, nullable=False)
    createdBy = Column(String(20))
    createdByName = Column(String(100))
    createdAt = Column(TIMESTAMP)
    updatedBy = Column(String(20))
    updatedByName = Column(String(100))
    updatedAt = Column(TIMESTAMP)


class UnNumber(Base):
    __tablename__ = "unNumber"
    __table_args__ = (
        Index("idx_unNumber_storageClass", "unNumber", "storageClassNumber"),
    )

    id = Column(String(20), primary_key=True)
    unNumber = Column(String(20))
    storageClassNumber = Column(VARCHAR(100))
    storageClassName = Column(String(255))
    unClassification = Column(VARCHAR(100))
    shippingDescription = Column(String(1000))
    status = Column(String(20))
    createdAt = Column(TIMESTAMP)
    createdBy = Column(VARCHAR(100), index=True)
    createdByName = Column(String(100))
    updatedAt = Column(TIMESTAMP)
    updatedBy = Column(VARCHAR(100), index=True)
    updatedByName = Column(String(100))


class Unit(Base):
    __tablename__ = "unit"

    id = Column(String(20), primary_key=True)
    name = Column(String(1000))
    category = Column(String(100))
    symbol = Column(String(1000))
    synonyms = Column(JSON)
    status = Column(String(20))
    verified = Column(String(20))
    createdAt = Column(TIMESTAMP)
    createdBy = Column(String(20), index=True)
    createdByName = Column(String(100))
    updatedAt = Column(TIMESTAMP)
    updatedBy = Column(String(20), index=True)
    updatedByName = Column(String(100))


class UserLocation(Base):
    __tablename__ = "userLocation"

    id = Column(VARCHAR(20), primary_key=True, nullable=False)
    parentId = Column(VARCHAR(20), primary_key=True, nullable=False, index=True)
    name = Column(String(100))
    createdBy = Column(String(20))
    createdByName = Column(String(100))
    createdAt = Column(TIMESTAMP)
    updatedBy = Column(String(20))
    updatedByName = Column(String(100))
    updatedAt = Column(TIMESTAMP)


class UserPersonalization(Base):
    __tablename__ = "userPersonalization"

    id = Column(String(200), primary_key=True, nullable=False)
    category = Column(String(300))
    createdAt = Column(DateTime)
    createdBy = Column(String(200))
    createdByName = Column(String(300))
    parentId = Column(String(200), primary_key=True, nullable=False)
    savedId = Column(String(300))
    savedName = Column(String(300))


class UserRole(Base):
    __tablename__ = "userRole"

    id = Column(VARCHAR(20), primary_key=True, nullable=False)
    parentId = Column(VARCHAR(20), primary_key=True, nullable=False, index=True)
    name = Column(String(100))
    createdBy = Column(String(20))
    createdByName = Column(String(100))
    createdAt = Column(TIMESTAMP)
    updatedBy = Column(String(20))
    updatedByName = Column(String(100))
    updatedAt = Column(TIMESTAMP)


class User(Base):
    __tablename__ = "users"

    id = Column(String(20), primary_key=True)
    name = Column(String(1000))
    _class = Column("class", String(100))
    lastLoginTime = Column(TIMESTAMP)
    isSSO = Column(TINYINT(1))
    email = Column(String(300))
    status = Column(VARCHAR(20))
    createdAt = Column(TIMESTAMP)
    createdBy = Column(String(20), index=True)
    createdByName = Column(String(100))
    updatedAt = Column(TIMESTAMP)
    updatedBy = Column(String(20), index=True)
    updatedByName = Column(String(100))
    Metadata = Column(JSON)


class Workflow(Base):
    __tablename__ = "workflow"

    id = Column(String(20), primary_key=True)
    name = Column(String(1000))
    workflow_old = Column(JSON)
    workflowSequence = Column(JSON)
    workflowHash = Column(String(50))
    status = Column(String(20))
    createdAt = Column(TIMESTAMP)
    createdBy = Column(String(20), index=True)
    createdByName = Column(String(100))
    updatedAt = Column(TIMESTAMP)
    updatedBy = Column(String(20), index=True)
    updatedByName = Column(String(100))
    workflow = Column(LONGBLOB)


class WorkflowInterval(Base):
    __tablename__ = "workflowInterval"
    __table_args__ = (
        Index("idx_parentRowId", "parentId", "rowId"),
        Index("idx_parentrowrowId", "parentId", "parentRowId", "rowId"),
    )

    id = Column(VARCHAR(20))
    rowId = Column(VARCHAR(10), primary_key=True, nullable=False)
    parentId = Column(VARCHAR(20), primary_key=True, nullable=False)
    parentRowId = Column(String(20))
    value = Column(VARCHAR(20))
    createdBy = Column(String(20))
    createdByName = Column(String(100))
    createdAt = Column(TIMESTAMP)
    updatedBy = Column(String(20))
    updatedByName = Column(String(100))
    updatedAt = Column(TIMESTAMP)


class WorkflowParameter(Base):
    __tablename__ = "workflowParameter"
    __table_args__ = (Index("idx_parentId_parentRowId", "parentId", "parentRowId"),)

    id = Column(VARCHAR(20))
    rowId = Column(VARCHAR(10), primary_key=True, nullable=False)
    parentId = Column(VARCHAR(20), primary_key=True, nullable=False)
    parentRowId = Column(VARCHAR(20))
    name = Column(String(100))
    value = Column(VARCHAR(100))
    createdBy = Column(String(20))
    createdByName = Column(String(100))
    createdAt = Column(TIMESTAMP)
    updatedBy = Column(String(20))
    updatedByName = Column(String(100))
    updatedAt = Column(TIMESTAMP)


class WorkflowParameterGroup(Base):
    __tablename__ = "workflowParameterGroup"
    __table_args__ = (
        Index("idx_parentId_rowId", "parentId", "rowId"),
        Index("idx_parentId_id", "parentId", "id"),
    )

    id = Column(VARCHAR(20))
    rowId = Column(VARCHAR(10), primary_key=True, nullable=False)
    parentId = Column(VARCHAR(20), primary_key=True, nullable=False)
    name = Column(String(100))
    prgSequence = Column(Integer)
    createdBy = Column(String(20))
    createdByName = Column(String(100))
    createdAt = Column(TIMESTAMP)
    updatedBy = Column(String(20))
    updatedByName = Column(String(100))
    updatedAt = Column(TIMESTAMP)


class WorkflowSpecialParameter(Base):
    __tablename__ = "workflowSpecialParameter"
    __table_args__ = (Index("idx_parentId_rowId", "parentId", "rowId"),)

    id = Column(VARCHAR(20))
    rowId = Column(VARCHAR(10), primary_key=True, nullable=False)
    parentId = Column(VARCHAR(20), primary_key=True, nullable=False)
    name = Column(VARCHAR(1000))
    value = Column(VARCHAR(100))
    createdBy = Column(String(20))
    createdByName = Column(String(100))
    createdAt = Column(TIMESTAMP)
    updatedBy = Column(String(20))
    updatedByName = Column(String(100))
    updatedAt = Column(TIMESTAMP)


class WorkflowUnit(Base):
    __tablename__ = "workflowUnit"
    __table_args__ = (Index("idx_parentId_rowId", "parentId", "rowId"),)

    id = Column(VARCHAR(20))
    rowId = Column(VARCHAR(10), primary_key=True, nullable=False)
    parentId = Column(VARCHAR(20), primary_key=True, nullable=False)
    name = Column(VARCHAR(100))
    createdBy = Column(String(20))
    createdByName = Column(String(100))
    createdAt = Column(TIMESTAMP)
    updatedBy = Column(String(20))
    updatedByName = Column(String(100))
    updatedAt = Column(TIMESTAMP)
